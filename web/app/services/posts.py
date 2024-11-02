from app.schemas.posts import PostDTO
from app.mappers.posts import PostMapper
from app.repositories import Repositories


class PostsService:
    def __init__(self, repositories: Repositories):
        self.repositories = repositories

    async def create(self, tags: list[str], text: str, title: str, user_id: int):
        """"""

        post = await self.repositories.posts().create(
            tags=tags,
            text=text,
            title=title,
            user_id=user_id,
        )

        return PostMapper.to_dto(post, is_liked=False)

    async def get_all(
        self,
        user_id: int | None,
        limit: int | None,
        offset: int | None,
        filters: list[dict] | None,
        sorters: list[dict] | None,
        q: str | None = None,
        tags: list[str] | None = None,
    ) -> tuple[list[PostDTO], int]:
        """"""

        posts, count = await self.repositories.posts().get_all(
            q=q,
            tags=tags,
            limit=limit,
            offset=offset,
            filters=filters,
            sorters=sorters,
        )

        if user_id is None:
            liked = {post.id: False for post in posts}
        else:
            liked = await self.repositories.posts().posts_liked(
                user_id=user_id,
                posts_ids=[post.id for post in posts]
            )

        return [PostMapper.to_dto(post, liked[post.id]) for post in posts], count

    async def get_by_id(self, _id: int, user_id: int | None) -> PostDTO | None:
        """"""

        post = await self.repositories.posts().get_by_id(_id=_id)
        if post is None:
            return None

        if user_id is None:
            liked = {post.id: False}
        else:
            liked = await self.repositories.posts().posts_liked(
                user_id=user_id,
                posts_ids=[post.id]
            )

        return PostMapper.to_dto(post, liked[post.id])

    async def update(self, _id: int, values: dict):
        """"""

        return await self.repositories.posts().update(_id=_id, values=values)

    async def delete(self, _id: int):
        """"""

        return await self.repositories.posts().delete(_id=_id)
