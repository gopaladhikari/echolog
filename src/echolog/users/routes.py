from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session

from ..core.database import get_session
from ..core.dependencies import get_current_user
from ..core.security import get_password_hash
from .controllers import UserController
from .models import Users
from .schemas import (
    ChangePassword,
    CreateUser,
    ForgotPassword,
    Login,
    ReadUser,
    ResetPassword,
    UpdateUser,
)

# Auth router for authentication endpoints
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# User router for user management endpoints
user_router = APIRouter(prefix="/users", tags=["Users"])


# Authentication Routes
@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=ReadUser
)
def register(
    user_data: CreateUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Register a new user."""
    return UserController.register_user(user_data, session)


@auth_router.post("/login", response_model=ReadUser)
def login(
    login_data: Login,
    session: Annotated[Session, Depends(get_session)],
    response: Response,
):
    """Login user and receive JWT token."""
    return UserController.login_user(
        login_data.email, login_data.password, session, response
    )


@auth_router.post("/forgot-password")
def forgot_password(
    forgot_data: ForgotPassword,
    session: Annotated[Session, Depends(get_session)],
):
    """Request password reset token."""
    return UserController.forgot_password(forgot_data.email, session)


@auth_router.post("/reset-password")
def reset_password(
    reset_data: ResetPassword,
    session: Annotated[Session, Depends(get_session)],
):
    """Reset password using token."""
    return UserController.reset_password(reset_data, session)


# User Management Routes (Protected)
@user_router.get("/me", response_model=ReadUser)
def get_current_user_info(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """Get current user information."""
    return current_user


@user_router.patch("/me", response_model=ReadUser)
def update_current_user(
    user_data: UpdateUser,
    current_user: Annotated[Users, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """Update current user information."""
    if user_data.full_name is not None:
        current_user.full_name = user_data.full_name
    if user_data.email is not None:
        current_user.email = user_data.email
    if user_data.password is not None:
        current_user.password = get_password_hash(user_data.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@user_router.post("/change-password")
def change_password(
    password_data: ChangePassword,
    current_user: Annotated[Users, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """Change current user password."""
    return UserController.change_password(current_user, password_data, session)


@user_router.get("/{user_id}", response_model=ReadUser)
def get_user(
    user_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """Get user by ID (protected route)."""
    return UserController.get_user_by_id(user_id, session)


@user_router.get("/", response_model=list[ReadUser])
def get_users(
    current_user: Annotated[Users, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """Get all users (protected route)."""
    from sqlmodel import select

    statement = select(Users)
    users = session.exec(statement).all()
    return users
