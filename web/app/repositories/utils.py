from typing import Type
from operator import eq, ne, ge, gt, le, lt

import sqlalchemy as sa
from sqlalchemy import Select

from app.db.models import Base


operators_map = {
    "eq": eq,
    "ne": ne,
    "ge": ge,
    "gt": gt,
    "le": le,
    "lt": lt,
    "in": lambda field, val: field.in_(val),
}


async def apply_filters(query, model: Type[Base], filters: list[dict]):
    """"""

    clauses = []
    for _filter in filters:

        field = getattr(model, _filter['field'])
        val, op = _filter['val'], _filter['operation']

        if val is None:
            if op == "eq":
                clauses.append(field.is_(None))
            elif op == "ne":
                clauses.append(field.isnot(None))
            else:
                raise ValueError("Incorrect operation used for None value")

        operation = operators_map[op]
        clauses.append(operation(field, val))

    return query.where(sa.and_(*clauses))


async def apply_sorters(query, model: Type[Base], sorters: list[dict]):

    for sorter in sorters:
        order, field = sorter["order"], sorter["field"]

        if order == "asc":
            query = query.order_by(getattr(model, sorter["field"]))
        elif order == "desc":
            query = query.order_by(getattr(model, sorter["field"]).desc())
        else:
            raise ValueError("GIVEN WRONG ORDER TYPE TO SORTERS")

    return query


async def get_all_query(
    model,
    query: Select,
    limit: int | None,
    offset: int | None,
    sorters: list[dict] | None,
    filters: list[dict] | None,
    text_search: tuple[str, str] | None = None,
) -> tuple[Select, Select]:
    """Returns query for getting object and count query

        :param model: any sqlalchemy model
        :param query: any Select query
        :param limit: number of objects to be returned
        :param offset: offset characteristics for the query
        :param sorters: sorting rules for current query
            example: {"created_at": "desc", "price": "asc"}
        :param filters: all filtering values which will apply AND logic
            example: {"price": 24.3}
        :param text_search: field and value for text search
            example: ("name", "ang")

    """

    count_query = sa.select(sa.func.count()).select_from(model)

    if filters:
        query = await apply_filters(
            model=model,
            query=query,
            filters=filters,
        )
        count_query = await apply_filters(
            model=model,
            query=count_query,
            filters=filters,
        )

    if text_search:
        field, value = text_search
        query = query.where(
            sa.text(f"{model.__tablename__}.{getattr(model, field).name} ILIKE '%{value}%'")
        )

    if sorters:
        query = await apply_sorters(
            model=model,
            query=query,
            sorters=sorters
        )

    if getattr(model, "deleted_at", None) is not None:
        query = query.where(model.deleted_at.is_(None))
        count_query = count_query.where(model.deleted_at.is_(None))

    query = query.limit(limit).offset(offset)

    return query, count_query
