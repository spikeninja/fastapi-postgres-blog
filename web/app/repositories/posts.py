import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import PostsModel, LikesModel
from app.repositories.generic import SqlAlchemyRepository


class PostsRepository:
    _repository: SqlAlchemyRepository[PostsModel]

    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = SqlAlchemyRepository[PostsModel](
            session=session,
            model=PostsModel,
        )

    async def get_all(
        self,
        limit: int | None,
        offset: int | None,
        filters: list[dict] | None,
        sorters: list[dict] | None,
        q: str | None = None,
    ) -> tuple[list[PostsModel], int]:
        """"""

        posts, count = await self._repository.get_all(
            q=q,
            limit=limit,
            offset=offset,
            filters=filters,
            sorters=sorters,
        )

        return posts, count

    async def get_by_id(self, _id: int) -> PostsModel | None:
        """"""

        post = await self._repository.get_by_id(_id=_id)
        if not post:
            return None

        return post

    async def create(
        self,
        text: str,
        title: str,
        user_id: int,
        tags: list[str],
    ) -> PostsModel:
        """"""

        post = PostsModel(
            tags=tags,
            text=text,
            title=title,
            user_id=user_id,
        )
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)

        return post

    async def update(self, _id: int, values: dict):
        """"""

        return await self._repository.update(_id=_id, values=values)

    async def delete(self, _id: int):
        """"""

        return await self._repository.delete(_id=_id)

    async def get_all_tags(self) -> set[str]:
        """"""

        query = sa.select(PostsModel.tags)
        all_tags = await self.session.scalars(query)
        # print("ALL TAGS: ", list(all_tags))

        unique_tags = set()
        for tag in all_tags:
            unique_tags.update(tag)

        return unique_tags

    async def like(self, post_id: int, user_id: int):
        """"""

        like = LikesModel(
            user_id=user_id,
            post_id=post_id
        )
        self.session.add(like)
        await self.session.commit()

    async def dislike(self, post_id: int, user_id: int):
        """"""

        like = await self.session.scalar(
            sa.select(LikesModel)
            .where(
                sa.and_(
                    LikesModel.post_id == post_id,
                    LikesModel.user_id == user_id,
                )
            )
        )

        await self.session.delete(like)
        await self.session.commit()

    async def get_like(self, post_id: int, user_id: int) -> LikesModel | None:
        """"""

        return await self.session.scalar(
            sa.select(LikesModel)
            .where(
                sa.and_(
                    LikesModel.post_id == post_id,
                    LikesModel.user_id == user_id,
                )
            )
        )

    async def posts_liked(self, user_id: int, posts_ids: list[int]) -> dict[int, bool]:
        """"""

        liked = {_id: False for _id in posts_ids}

        query = (
            sa.select(LikesModel.post_id)
            .where(
                sa.and_(
                    LikesModel.user_id == user_id,
                    LikesModel.post_id.in_(posts_ids),
                )
            )
        )
        results = await self.session.scalars(query)

        for post_id in results:
            liked[post_id] = True

        return liked
