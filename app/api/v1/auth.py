from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.database import AsyncDB
from app.core.dependencies import CurrentUser
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
async def register(data: RegisterRequest, db: AsyncDB) -> TokenResponse:
    try:
        return await AuthService(db).register(data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncDB) -> TokenResponse:
    try:
        return await AuthService(db).login(data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err)
        ) from err


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser, db: AsyncDB) -> UserResponse:

    user = await db.scalar(select(User).where(User.id == current_user["user_id"]))
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return UserResponse.model_validate(user)
