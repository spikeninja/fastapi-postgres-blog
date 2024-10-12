from fastapi import APIRouter, HTTPException, status, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.schemas.users import UserDTO
from app.repositories import Repositories
from app.schemas.mixins import ResponseItems
from app.api.dependencies import get_current_user
from app.schemas.comments import CommentUpdateRequest, CommentPublic

router = APIRouter(prefix="/comments", route_class=DishkaRoute)


@router.get("/", response_model=ResponseItems[CommentPublic])
async def get_all(
    repositories: FromDishka[Repositories],
    q: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    post_id: int | None = None,
):
    """"""

    comments, count = await repositories.comments().get_all(
        q=q,
        limit=limit,
        offset=offset,
        filters=[{
            "field": "post_id",
            "operation": "eq",
            "val": post_id,
        }] if post_id else None,
        sorters=[{"order": "desc", "field": "created_at"}],
    )

    return {"items": comments, "count": count}


@router.get("/{_id}", response_model=CommentPublic)
async def get_by_id(_id: int, repositories: FromDishka[Repositories]):
    """"""

    comment_db = await repositories.comments().get_by_id(_id=_id)
    if not comment_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={_id} is not found"
        )

    return comment_db


@router.patch("/{_id}", response_model=CommentPublic)
async def update(
    _id: int,
    request: CommentUpdateRequest,
    repositories: FromDishka[Repositories],
    current_user: UserDTO = Depends(get_current_user),
):
    """"""

    comment_db = await repositories.comments().get_by_id(_id=_id)
    if not comment_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={_id} is not found"
        )

    if current_user.id != comment_db.author.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You cannot update not your comments"
        )

    values = request.model_dump(exclude_unset=True)
    if not values:
        return comment_db

    await repositories.comments().update(_id=_id, values=values)

    return await repositories.comments().get_by_id(_id=_id)


@router.delete("/{_id}", response_model=CommentPublic)
async def delete(
    _id: int,
    repositories: FromDishka[Repositories],
    current_user: UserDTO = Depends(get_current_user),
):
    """"""

    comment_db = await repositories.comments().get_by_id(_id=_id)
    if not comment_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={_id} is not found"
        )

    if comment_db.author.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have no access to this resourse"
        )

    await repositories.comments().delete(_id=_id)

    return comment_db
