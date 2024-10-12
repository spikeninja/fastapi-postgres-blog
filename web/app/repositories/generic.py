from typing import Type

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Base
from app.utils.functions import utcnow
from app.repositories.utils import get_all_query


class SqlAlchemyRepository[Model: Base]:

    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(
        self,
        limit: int | None,
        offset: int | None,
        filters: list[dict] | None,
        sorters: list[dict] | None,
        q: str | None = None,
    ) -> tuple[list[Model], int]:
        """"""

        items_query, count_query = await get_all_query(
            model=self.model,
            filters=filters,
            sorters=sorters,
            limit=limit,
            offset=offset,
            text_search=q,
            query=select(self.model),
        )

        items = await self.session.scalars(items_query)
        count = await self.session.scalar(count_query)

        return list(items), count

    async def get_by_id(self, _id: int) -> Model | None:
        """"""

        query = select(self.model).where(self.model.id == _id)

        return await self.session.scalar(query)

    async def update(self, _id: int, values: dict):
        """"""

        now_ = utcnow()

        query = (
            update(self.model)
            .where(self.model.id == _id)
            .values({
                **values,
                "updated_at": now_,
            })
        )

        await self.session.execute(query)
        await self.session.commit()

    async def delete(self, _id: int):
        """"""

        query = delete(self.model).where(self.model.id == _id)

        await self.session.execute(query)
        await self.session.commit()
