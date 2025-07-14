#!/usr/bin/python3
"""Auth Route module"""

from app.api.v1.schemas.auth import UserCreate, UserRead
from app.core.security import create_access_token
from app.db.session import get_session
from app.services.auth_service import Auth_Service, get_google_user, oauth
from fastapi.responses import RedirectResponse
from app.core.config import get_settings
from fastapi import Depends, Request, APIRouter, status
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter()
settings = get_settings()


@router.get("/google/login")
async def google_login(request: Request):
    """login with google"""
    redirect_url = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_url)

@router.get("/google/callback")
async def google_callback(request: Request):
    user = await get_google_user(request)
    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"email": user.email, "name": user.full_name, "picture": user.picture},
    }

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """Register new user"""
    auth_service = Auth_Service(session)
    user = await auth_service.register_user(user_data)
    return user
