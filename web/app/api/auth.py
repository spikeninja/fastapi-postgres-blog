from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.core.config import settings
from app.repositories import Repositories
from app.schemas.auth import LoginRequest, AuthResponse, RegisterRequest
from app.core.security import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/auth", route_class=DishkaRoute)


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    repositories: FromDishka[Repositories],
):
    """"""

    db_user = await repositories.users().get_by_email(email=request.email)
    if not db_user:
        raise HTTPException(
            detail="User with such email does not exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    password_verified = await verify_password(request.password, db_user.hashed_password)

    if not password_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials"
        )

    token = await create_access_token(
        payload={'sub': db_user.id},
        minutes=settings.access_token_expire_minutes
    )

    return {"token": token, "user": db_user}


@router.post("/register", response_model=AuthResponse)
async def register(
    request: RegisterRequest,
    repositories: FromDishka[Repositories],
):
    """"""

    db_user = await repositories.users().get_by_email(email=request.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists."
        )

    hashed_password = await hash_password(password=request.password)
    user = await repositories.users().create(
        email=request.email,
        name=request.name,
        hashed_password=hashed_password,
    )

    token = await create_access_token(
        payload={"sub": user.id},
        minutes=settings.access_token_expire_minutes,
    )

    return {"token": token, "user": user}
