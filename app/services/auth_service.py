#!/usr/bin/python3
"""Auth Service module"""

from authlib.integrations.starlette_client import OAuth
from app.core.config import get_settings
from app.db.session import get_session
from sqlmodel import select
from fastapi import HTTPException, status, Request
from app.db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, verify_password, create_access_token
from typing import Optional
from datetime import datetime, UTC

from app.schemas.auth import Token, UserCreate, UserLogin



settings = get_settings()
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)

async def get_google_user(request: Request) -> User:
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info or not user_info.get("email_verified"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified by Google",
        )

    async for session in get_session():
        result = await session.exec(
            select(User).where(User.email == user_info["email"])
        )
        user = result.first()

        if user:
            return user

        user = User(
            email=user_info["email"],
            full_name=user_info.get("name"),
            picture=user_info.get("picture"),
            is_verified=True,
            provider="google",
            google_sub=user_info.get("sub"),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        break

    return user

class Auth_Service:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_user(self, data: UserCreate) -> User:
        userExists = await self.session.exec(
            select(User).where(User.email == data.email)
            )
        if userExists.first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists."
                )
        
        hashed_password = hash_password(data.password)
        
        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False,
            provider="email",
            role="user"
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def authenticate_user(self, data: UserLogin) -> Optional[User]:
        result = await self.session.exec(
            select(User).where(User.email == data.email)
            )
        user = result.first()

        if not user or not verify_password(data.password, user.hashed_password):
            return None
        return user

def utcnow():
    """Return a timezone-aware UTC datetime."""
    return datetime.now(UTC)
