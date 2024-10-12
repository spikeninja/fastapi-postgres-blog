from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.models import UsersModel
from app.repositories import Repositories
from app.api.dependencies import get_current_user
from app.core.security import verify_password, hash_password
from app.schemas.users import UserPublic, UserUpdate, PasswordUpdate


router = APIRouter(prefix="/users", route_class=DishkaRoute)


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: UsersModel = Depends(get_current_user)):
    """"""

    return current_user


@router.patch("/me", response_model=UserPublic)
async def update_me(
    request: UserUpdate,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user)
):
    """"""

    await repositories.users().update(
        _id=current_user.id,
        values=request.model_dump(exclude_unset=True)
    )

    return await repositories.users().get_by_id(_id=current_user.id)


@router.post("/me/password", response_model=UserPublic)
async def change_password(
    request: PasswordUpdate,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user)
):
    """"""

    password_correct = await verify_password(
        password=request.old_password,
        hashed=current_user.hashed_password,
    )

    if not password_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect operation"
        )

    if request.new_password == request.old_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password should be different"
        )

    new_hashed = await hash_password(password=request.new_password)

    await repositories.users().update(
        _id=current_user.id,
        values={
            "hashed_password": new_hashed,
        }
    )

    return await repositories.users().get_by_id(_id=current_user.id)


@router.get("/{user_id}", response_model=UserPublic)
async def get_by_id(
    user_id: int,
    repositories: FromDishka[Repositories]
):
    """"""

    return await repositories.users().get_by_id(_id=user_id)
