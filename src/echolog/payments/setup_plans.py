import os

import requests
from dotenv import load_dotenv
from paypalserversdk.configuration import Environment
from paypalserversdk.http.auth.o_auth_2 import ClientCredentialsAuthCredentials
from paypalserversdk.models.frequency import Frequency
from paypalserversdk.models.money import Money
from paypalserversdk.models.payment_preferences import PaymentPreferences
from paypalserversdk.models.plan_request import PlanRequest
from paypalserversdk.models.subscription_billing_cycle import SubscriptionBillingCycle
from paypalserversdk.models.subscription_pricing_scheme import SubscriptionPricingScheme
from paypalserversdk.paypal_serversdk_client import PaypalServersdkClient

load_dotenv()
CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_API = "https://api-m.sandbox.paypal.com"


paypal = PaypalServersdkClient(
    client_credentials_auth_credentials=ClientCredentialsAuthCredentials(
        o_auth_client_id=CLIENT_ID,
        o_auth_client_secret=CLIENT_SECRET,
    ),
    environment=Environment.SANDBOX,
)


def get_access_token() -> str:
    res = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        auth=(CLIENT_ID, CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
        timeout=10,
    )
    res.raise_for_status()
    return res.json()["access_token"]


def create_product() -> str:

    res = requests.post(
        f"{PAYPAL_API}/v1/catalogs/products",
        headers={
            "Authorization": f"Bearer {get_access_token()}",
            "Content-Type": "application/json",
        },
        json={
            "name": "EchoLog Pro",
            "description": "Premium Trading Journal Subscription",
            "type": "SERVICE",
            "category": "SOFTWARE",
        },
        timeout=10,
    )
    res.raise_for_status()
    return res.json()["id"]


def create_plan(product_id: str, plan_name: str, interval_unit: str, price: str) -> str:

    plan = paypal.subscriptions.create_billing_plan(
        {
            "body": PlanRequest(
                product_id=product_id,
                name=plan_name,
                billing_cycles=[
                    SubscriptionBillingCycle(
                        tenure_type="REGULAR",
                        sequence=1,
                        total_cycles=0,
                        frequency=Frequency(
                            interval_unit=interval_unit, interval_count=1
                        ),
                        pricing_scheme=SubscriptionPricingScheme(
                            fixed_price=Money(currency_code="USD", value=price)
                        ),
                    )
                ],
                payment_preferences=PaymentPreferences(
                    auto_bill_outstanding=True, payment_failure_threshold=3
                ),
            ),
            "prefer": "return=representation",
        }
    )
    return plan.body.id


if __name__ == "__main__":
    print("Initializing EchoLog PayPal Setup...")

    # 1. Create the Base Product
    product_id = create_product()
    print(f"✅ Product Created: {product_id}")

    # 2. Create the $20 Monthly Plan
    monthly_plan_id = create_plan(product_id, "EchoLog Pro - Monthly", "MONTH", "20.00")
    print(f"✅ Monthly Plan ID Generated: {monthly_plan_id}")

    # 3. Create the $200 Yearly Plan
    yearly_plan_id = create_plan(product_id, "EchoLog Pro - Yearly", "YEAR", "200.00")
    print(f"✅ Yearly Plan ID Generated: {yearly_plan_id}")

    print("\n🎉 Setup Complete! Copy and paste the following into your .env file:\n")
    print(f"PAYPAL_MONTHLY_PLAN_ID={monthly_plan_id}")
    print(f"PAYPAL_YEARLY_PLAN_ID={yearly_plan_id}")
