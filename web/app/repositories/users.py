import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UsersModel
from app.schemas.users import UserDTO
from app.repositories.generic import SqlAlchemyRepository


class UsersRepository:
    _repository: SqlAlchemyRepository[UsersModel]

    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = SqlAlchemyRepository[UsersModel](
            session=session,
            model=UsersModel,
        )

    async def __mapper(self, user: UsersModel) -> UserDTO:
        """"""

        return UserDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at,
            hashed_password=user.hashed_password,
        )

    async def get_by_id(self, _id: int) -> UserDTO | None:
        """"""

        user = await self._repository.get_by_id(_id=_id)
        if not user:
            return None

        return await self.__mapper(user=user)

    async def get_by_email(self, email: str) -> UserDTO | None:
        """"""

        query = sa.select(UsersModel).where(UsersModel.email == email)

        user = await self.session.scalar(query)
        if not user:
            return None

        return await self.__mapper(user=user)

    async def create(self, email: str, name: str, hashed_password: str) -> UserDTO:
        """"""

        user = UsersModel(
            name=name,
            email=email,
            hashed_password=hashed_password,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return await self.__mapper(user=user)

    async def update(self, _id: int, values: dict):
        """"""

        return await self._repository.update(_id=_id, values=values)
