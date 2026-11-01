from datetime import UTC, datetime

import requests
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from paypalserversdk.configuration import Environment
from paypalserversdk.http.auth.o_auth_2 import ClientCredentialsAuthCredentials
from paypalserversdk.models.create_subscription_request import CreateSubscriptionRequest
from paypalserversdk.paypal_serversdk_client import PaypalServersdkClient
from sqlmodel import Session, select

from echolog.core.config import config
from echolog.payments.models import Subscription
from echolog.users.models import Users

PAYPAL_API = "https://api-m.sandbox.paypal.com"

paypal_client = PaypalServersdkClient(
    client_credentials_auth_credentials=ClientCredentialsAuthCredentials(
        o_auth_client_id=config.PAYPAL_CLIENT_ID,
        o_auth_client_secret=config.PAYPAL_CLIENT_SECRET,
    ),
    environment=Environment.SANDBOX,
)


def get_access_token():
    res = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        auth=(config.PAYPAL_CLIENT_ID, config.PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
        timeout=10,
    )

    return res.json()["access_token"]


class PaymentController:
    """Controller for payment and subscription operations."""

    @staticmethod
    def create_checkout_session(user: Users, interval: str) -> str:

        plan_id = (
            config.PAYPAL_MONTHLY_PLAN_ID
            if interval == "monthly"
            else config.PAYPAL_YEARLY_PLAN_ID
        )

        subscription = paypal_client.subscriptions.create_subscription(
            {
                "body": CreateSubscriptionRequest(
                    {
                        "plan_id": plan_id,
                        "custom_id": str(user.id),
                        "application_context": {
                            "brand_name": "EchoLog",
                            "return_url": "url/payment/success",
                            "cancel_url": "url/payment/cancel",
                            "user_action": "SUBSCRIBE_NOW",
                        },
                    }
                ),
                "prefer": "return=representation",
            }
        )

        for link in subscription.body.links:
            if link.rel == "approve":
                return RedirectResponse(url=link.href)

        raise HTTPException(status_code=500, detail="Approval URL not found")

    @staticmethod
    def cancel_subscription(user: Users):
        paypal_client.subscriptions.cancel_subscription(
            {
                "id": user.subscription.provider_subscription_id,
                "body": {"reason": "Cancelled by user"},
            }
        )

        return RedirectResponse(url="/")

    @staticmethod
    def process_webhook(headers: dict, event: dict, session: Session) -> None:
        """Verify PayPal signature and update the database based on the event."""

        # 1. Get an Access Token to verify the signature
        auth_response = requests.post(
            "https://api-m.sandbox.paypal.com/v1/oauth2/token",
            auth=(config.PAYPAL_CLIENT_ID, config.PAYPAL_CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
            timeout=10,
        )
        auth_response.raise_for_status()
        access_token = auth_response.json()["access_token"]

        # 2. Verify the Webhook Signature with PayPal
        verify_response = requests.post(
            "https://api-m.sandbox.paypal.com/v1/notifications/verify-webhook-signature",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={
                "transmission_id": headers.get("paypal-transmission-id"),
                "transmission_time": headers.get("paypal-transmission-time"),
                "cert_url": headers.get("paypal-cert-url"),
                "auth_algo": headers.get("paypal-auth-algo"),
                "transmission_sig": headers.get("paypal-transmission-sig"),
                "webhook_id": config.PAYPAL_WEBHOOK_ID,
                "webhook_event": event,
            },
            timeout=10,
        )

        if verify_response.json().get("verification_status") != "SUCCESS":
            raise HTTPException(status_code=400, detail="Invalid webhook signature")

        # 3. Process the Verified Event
        event_type = event.get("event_type")

        resource = event.get("resource", {})

        user_id_str = resource.get("custom_id")

        if not user_id_str:
            return

        user_id = int(user_id_str)

        sub_id = resource.get("id")

        if event_type == "BILLING.SUBSCRIPTION.ACTIVATED":
            payer_id = resource.get("subscriber", {}).get("payer_id", "")

            new_sub = Subscription(
                user_id=user_id,
                provider="paypal",
                provider_customer_id=payer_id,
                provider_subscription_id=sub_id,
                status="active",
                plan_tier="pro",
                current_period_end=datetime.now(UTC),
                cancel_at_period_end=False,
            )
            session.add(new_sub)
            session.commit()

        elif event_type in [
            "BILLING.SUBSCRIPTION.CANCELLED",
            "BILLING.SUBSCRIPTION.EXPIRED",
            "BILLING.SUBSCRIPTION.SUSPENDED",
        ]:
            statement = select(Subscription).where(
                Subscription.provider_subscription_id == sub_id
            )

            sub = session.exec(statement).first()

            if sub:
                sub.status = "canceled"
                session.add(sub)
                session.commit()
