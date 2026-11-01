from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from echolog.core.database import get_session
from echolog.core.dependencies import get_current_user
from echolog.users.models import Users

from .controllers import PaymentController

payments_router = APIRouter(prefix="/payments", tags=["Payments"])

CurrentUser = Annotated[Users, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_session)]


@payments_router.post("/checkout")
def create_checkout_session(current_user: CurrentUser):
    """Generate a PayPal checkout URL for the user."""
    checkout_url = PaymentController.create_checkout_session(current_user)
    return {"checkout_url": checkout_url}


@payments_router.post("/webhook")
async def paypal_webhook(request: Request, db: DB):
    """Listen for events from PayPal and update the database."""

    event = await request.json()

    PaymentController.process_webhook(dict(request.headers), event, db)

    return {"status": "success"}
