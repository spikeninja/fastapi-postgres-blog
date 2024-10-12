from enum import Enum
from typing import TypeVar, List, Generic

from pydantic import BaseModel

T = TypeVar("T")


class ResponseItems(BaseModel, Generic[T]):
    count: int
    items: List[T]


# Filters, Sorters
class OrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class SorterBase(BaseModel):
    field: str
    order: OrderEnum


class OperationEnum(str, Enum):
    eq = "eq"
    ne = "ne"
    gt = "gt"
    ge = "ge"
    lt = "lt"
    le = "le"
    in_ = "in"


class FilterBase(BaseModel):
    operation: OperationEnum
    val: list | float | int | bool | str | None
