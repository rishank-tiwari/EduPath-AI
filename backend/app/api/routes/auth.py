"""
FastAPI Route Endpoints for User Authentication & Authorization.
"""

from typing import Optional
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field
from app.core.database import DatabaseConnectionError
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication & Auth"])


class LoginRequest(BaseModel):
    username_or_email: str = Field(..., description="Username or email address")
    password: str = Field(..., description="User password")


class RegisterRequest(BaseModel):
    username: str = Field(..., description="Desired username")
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class AuthResponse(BaseModel):
    user_id: str
    username: str
    email: str
    access_token: str
    token_type: str = "bearer"


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Log In User",
    description="Authenticates credentials and returns JWT access token.",
)
def login(payload: LoginRequest):
    try:
        return auth_service.login_user(payload.username_or_email, payload.password)
    except HTTPException:
        raise
    except DatabaseConnectionError as db_err:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(db_err))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Login failed: {str(e)}")


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Creates a new learner account and returns JWT access token.",
)
def register(payload: RegisterRequest):
    try:
        return auth_service.register_user(payload.username, payload.email, payload.password)
    except HTTPException:
        raise
    except DatabaseConnectionError as db_err:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(db_err))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Registration failed: {str(e)}")


@router.get(
    "/me",
    summary="Get Current Authenticated User",
    description="Validates Bearer token and returns current user info.",
)
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header.")
    
    token = authorization.split(" ")[1]
    payload = auth_service.verify_jwt_token(token)
    return {
        "user_id": payload["sub"],
        "email": payload["email"],
        "authenticated": True,
    }
