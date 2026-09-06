from datetime import timedelta
from fastapi import Response
from sqlmodel import Session, select

from ..core.config import config
from ..core.jwt import create_access_token, verify_token
from ..core.security import get_password_hash, verify_password
from .exceptions import (
    IncorrectPasswordException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from .models import Users
from .schemas import ChangePassword, CreateUser, ResetPassword


class UserController:
    """Controller for user-related operations."""

    @staticmethod
    def register_user(user_data: CreateUser, session: Session) -> Users:
        """Register a new user with hashed password."""
        # Check if user already exists

        statement = select(Users).where(Users.email == user_data.email)

        existing_user = session.exec(statement).first()

        if existing_user:
            raise UserAlreadyExistsException(user_data.email)

        new_user = Users.model_validate(user_data)

        # Hash password before saving
        hashed_password = get_password_hash(user_data.password)

        # Create new user
        new_user.password = hashed_password

        session.add(new_user)

        session.commit()

        session.refresh(new_user)

        return new_user

    @staticmethod
    def login_user(
        email: str, password: str, session: Session, response: Response
    ) -> dict:
        """Login user and return JWT token."""
        statement = select(Users).where(Users.email == email)

        user = session.exec(statement).first()

        if not user:
            raise UserNotFoundException()

        if not verify_password(password, user.password):
            raise IncorrectPasswordException()

        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=3600,
            httponly=True,
            secure=True,
            samesite="lax",
        )

        return user

    @staticmethod
    def change_password(
        user: Users, password_data: ChangePassword, session: Session
    ) -> dict:
        """Change user password."""
        # Verify current password
        if not verify_password(password_data.current_password, user.password):
            raise IncorrectPasswordException()

        # Hash new password
        hashed_password = get_password_hash(password_data.new_password)

        # Update password
        user.password = hashed_password
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"message": "Password changed successfully"}

    @staticmethod
    def forgot_password(email: str, session: Session) -> dict:
        """Generate password reset token."""
        statement = select(Users).where(Users.email == email)
        user = session.exec(statement).first()

        if not user:
            # Don't reveal if user exists or not for security
            return {"message": "If user exists, password reset email sent"}

        # Create reset token with short expiration
        reset_token_expires = timedelta(
            minutes=config.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
        )
        reset_token = create_access_token(
            data={"sub": user.email, "type": "password_reset"},
            expires_delta=reset_token_expires,
        )

        # In production, you would send this via email
        return {
            "message": "Password reset token generated",
            "reset_token": reset_token,  # Remove this in production
        }

    @staticmethod
    def reset_password(reset_data: ResetPassword, session: Session) -> dict:
        """Reset password using token."""
        # Verify token
        payload = verify_token(reset_data.token)

        if payload is None:
            raise InvalidTokenException()

        # Check if it's a password reset token
        if payload.get("type") != "password_reset":
            raise InvalidTokenException()

        email = payload.get("sub")
        if email is None:
            raise InvalidTokenException()

        # Find user
        statement = select(Users).where(Users.email == email)
        user = session.exec(statement).first()

        if not user:
            raise UserNotFoundException(email)

        # Hash new password
        hashed_password = get_password_hash(reset_data.new_password)

        # Update password
        user.password = hashed_password
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"message": "Password reset successfully"}

    @staticmethod
    def get_user_by_email(email: str, session: Session) -> Users:
        """Get user by email."""
        statement = select(Users).where(Users.email == email)
        user = session.exec(statement).first()

        if not user:
            raise UserNotFoundException(email)

        return user

    @staticmethod
    def get_user_by_id(user_id: int, session: Session) -> Users:
        """Get user by ID."""
        user = session.get(Users, user_id)

        if not user:
            raise UserNotFoundException(str(user_id))

        return user
