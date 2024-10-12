from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import CommentsModel
from app.repositories.generic import SqlAlchemyRepository
from app.schemas.comments import CommentDTO, CommentUser, CommentPost


class CommentsRepository:
    _repository: SqlAlchemyRepository[CommentsModel]

    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = SqlAlchemyRepository[CommentsModel](
            session=session,
            model=CommentsModel,
        )

    async def __mapper(self, comment: CommentsModel) -> CommentDTO:
        """"""

        return CommentDTO(
            id=comment.id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            text=comment.text,
            user_id=comment.user_id,
            post_id=comment.post_id,
            author=CommentUser(
                id=comment.author.id,
                created_at=comment.author.created_at,
                updated_at=comment.author.updated_at,
                name=comment.author.name,
                email=comment.author.email,
            ),
            post=CommentPost(
                id=comment.post.id,
                user_id=comment.post.user_id,
                created_at=comment.post.created_at,
                updated_at=comment.post.updated_at,
                author=CommentUser(
                    id=comment.post.author.id,
                    created_at=comment.post.author.created_at,
                    updated_at=comment.post.author.updated_at,
                    name=comment.post.author.name,
                    email=comment.post.author.email,
                )
            ),
        )

    async def get_all(
        self,
        limit: int | None,
        offset: int | None,
        filters: list[dict] | None,
        sorters: list[dict] | None,
        q: str | None = None,
    ) -> tuple[list[CommentDTO], int]:
        """"""

        comments, count = await self._repository.get_all(
            q=q,
            limit=limit,
            offset=offset,
            filters=filters,
            sorters=sorters,
        )

        return [await self.__mapper(comment=comment) for comment in comments], count

    async def get_by_id(self, _id: int) -> CommentDTO | None:
        """"""

        comment = await self._repository.get_by_id(_id=_id)
        if not comment:
            return None

        return await self.__mapper(comment=comment)

    async def create(
        self,
        text: str,
        user_id: int,
        post_id: int,
    ) -> CommentDTO:
        """"""

        comment = CommentsModel(
            text=text,
            user_id=user_id,
            post_id=post_id,
        )

        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)

        return await self.__mapper(comment=comment)

    async def update(self, _id: int, values: dict) -> CommentsModel:
        """"""

        return await self._repository.update(_id=_id, values=values)

    async def delete(self, _id: int):
        """"""

        return await self._repository.delete(_id=_id)
