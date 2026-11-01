from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from echolog.core.database import get_session
from echolog.core.dependencies import get_current_user
from echolog.users.models import Users

from .controllers import PaymentController
from .schemas import CheckoutRequest

payments_router = APIRouter(prefix="/payments", tags=["Payments"])

CurrentUser = Annotated[Users, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_session)]


@payments_router.post("/checkout")
def create_checkout_session(request: CheckoutRequest, current_user: CurrentUser):
    """Generate a PayPal checkout URL for the user's chosen plan."""
    return PaymentController.create_checkout_session(current_user, request.interval)


@payments_router.post("/webhook")
async def paypal_webhook(request: Request, db: DB):
    """Listen for events from PayPal and update the database."""

    event = await request.json()

    PaymentController.process_webhook(dict(request.headers), event, db)

    return {"status": "success"}


@payments_router.post("/cancel")
async def cancel_subscription(current_user: CurrentUser):
    return PaymentController.cancel_subscription(current_user)
