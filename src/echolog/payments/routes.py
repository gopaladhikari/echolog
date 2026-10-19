from typing import Annotated

import stripe
from fastapi import APIRouter, Depends

from echolog.core.config import config
from echolog.core.dependencies import get_current_user
from echolog.users.models import Users

stripe.api_key = config.STRIPE_SECRET_KEY
payments_router = APIRouter(prefix="/payments", tags=["Payments"])

CurrentUser = Annotated[Users, Depends(get_current_user)]


@payments_router.post("/checkout")
def create_checkout_session(current_user: CurrentUser):
    """Generate a Stripe checkout URL for the user."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        customer_email=current_user.email,
        line_items=[{"price": "price_your_stripe_price_id_here", "quantity": 1}],
        success_url="https://yourfrontend.com/success",
        cancel_url="https://yourfrontend.com/cancel",
        # Pass the user ID so the webhook knows who paid!
        client_reference_id=str(current_user.id),
    )
    return {"checkout_url": session.url}
