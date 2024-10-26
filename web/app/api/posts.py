from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.db.models import UsersModel
from app.repositories import Repositories
from app.schemas.mixins import ResponseItems
from app.api.dependencies import get_current_user
from app.schemas.posts import PostCreateRequest, PostUpdateRequest, PostPublic
from app.schemas.comments import CommentCreateRequest, CommentPublic, CommentUpdateRequest

router = APIRouter(prefix="/posts", route_class=DishkaRoute)


@router.get("/")
async def get_all(
    repositories: FromDishka[Repositories],
    q: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    author_id: int | None = None,
    # tags: list[str] = Query(None, alias="tags"),
) -> ResponseItems[PostPublic]:
    """"""

    posts, count = await repositories.posts().get_all(
        q=q,
        limit=limit,
        offset=offset,
        filters=[{
            "field": "user_id",
            "val": author_id,
            "operation": "eq",
        }] if author_id else None,
        sorters=None,
    )

    return ResponseItems(count=count, items=posts)


@router.get("/tags")
async def get_all_tags(repositories: FromDishka[Repositories]):
    """"""

    tags = await repositories.posts().get_all_tags()

    return {"tags": tags}


@router.get("/{_id}", response_model=PostPublic)
async def get_by_id(
    _id: int,
    repositories: FromDishka[Repositories]
):
    """"""

    post_db = await repositories.posts().get_by_id(_id=_id)
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={_id} is not found"
        )

    return post_db


@router.post("/", response_model=PostPublic)
async def create_post(
    request: PostCreateRequest,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user),
):
    """"""

    return await repositories.posts().create(
        tags=request.tags,
        text=request.text,
        title=request.title,
        user_id=current_user.id,
    )


@router.patch("/{_id}", response_model=PostPublic)
async def update(
    _id: int,
    request: PostUpdateRequest,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user),
):
    """"""

    post_db = await repositories.posts().get_by_id(_id=_id)
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={_id} is not found"
        )

    if post_db.author.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can edit only your posts"
        )

    values = request.model_dump(exclude_unset=True)
    if not values:
        return post_db

    await repositories.posts().update(_id=_id, values=values)
    return await repositories.posts().get_by_id(_id=_id)


@router.delete("/{_id}", response_model=PostPublic)
async def delete(
    _id: int,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user),
):
    """"""

    post_db = await repositories.posts().get_by_id(_id=_id)
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={_id} is not found"
        )

    if post_db.author.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can delete only your posts"
        )

    await repositories.posts().delete(_id=_id)

    return post_db


@router.post("/{_id}/like", response_model=PostPublic)
async def like_post(
    _id: int,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user),
):
    """"""

    like = await repositories.posts().get_like(
        post_id=_id,
        user_id=current_user.id,
    )

    if like is not None:
        raise HTTPException(
            detail="You have already liked this post",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    await repositories.posts().like(post_id=_id, user_id=current_user.id)

    return await repositories.posts().get_by_id(_id=_id)


@router.delete("/{_id}/like")
async def dislike_post(
    _id: int,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user),
):
    """"""

    like = await repositories.posts().get_like(
        post_id=_id,
        user_id=current_user.id,
    )

    if not like:
        raise HTTPException(
            detail="You haven't like this post yet to delete it",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    await repositories.posts().dislike(post_id=_id, user_id=current_user.id)

    return await repositories.posts().get_by_id(_id=_id)


@router.get("/{_id}/comments", response_model=ResponseItems[CommentPublic])
async def get_comments(
    _id: int,
    limit: int,
    offset: int,
    repositories: FromDishka[Repositories],
):
    """"""

    post = await repositories.posts().get_by_id(_id=_id)
    if not post:
        raise HTTPException(
            detail=f"Post with id={_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    comments, count = await repositories.comments().get_all(
        limit=limit,
        offset=offset,
        sorters=[{"field": "created_at", "order": "desc"}],
        filters=[{
            "operation": "eq",
            "field": "post_id",
            "val": _id,
        }],
    )

    return {"items": comments, "count": count}


@router.post("/{_id}/comments", response_model=CommentPublic)
async def create_comment(
    _id: int,
    request: CommentCreateRequest,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user),
):
    """"""

    post = await repositories.posts().get_by_id(_id=_id)
    if not post:
        raise HTTPException(
            detail=f"Post with id={_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return await repositories.comments().create(
        post_id=post.id,
        text=request.text,
        user_id=current_user.id,
    )


@router.patch("/{_id}/comments/{comment_id}", response_model=CommentPublic)
async def update_comment(
    _id: int,
    comment_id: int,
    request: CommentUpdateRequest,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user),
):
    """"""

    post = await repositories.posts().get_by_id(_id=_id)
    if not post:
        raise HTTPException(
            detail=f"Post with id={_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    comment = await repositories.comments().get_by_id(_id=comment_id)
    if not comment:
        raise HTTPException(
            detail=f"Post with id={_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if current_user.id != comment.author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your comments"
        )

    await repositories.comments().update(
        _id=comment_id,
        values=request.model_dump(exclude_unset=True),
    )

    return await repositories.comments().get_by_id(_id=comment_id)


@router.delete("/{_id}/comments/{comment_id}", response_model=CommentPublic)
async def delete_comment(
    _id: int,
    comment_id: int,
    repositories: FromDishka[Repositories],
    current_user: UsersModel = Depends(get_current_user),
):
    """"""

    post = await repositories.posts().get_by_id(_id=_id)
    if not post:
        raise HTTPException(
            detail=f"Post with id={_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    comment = await repositories.comments().get_by_id(_id=comment_id)
    if not comment:
        raise HTTPException(
            detail=f"Post with id={_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if current_user.id != comment.author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your comments"
        )

    await repositories.comments().delete(_id=comment_id)

    return comment
