from typing import List
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import String, Index, text, ForeignKey, ColumnElement, Integer, type_coerce

from app.db.resources import Base
from app.utils.functions import utcnow


class UsersModel(Base):
    __tablename__ = "users"

    __table_args__ = (
        # for soft-delete mechanism
        Index(
            "idx_users__email__deleted_at",
            "email",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow)

    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

    email: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    hashed_password: Mapped[str] = mapped_column(String(256))


class LikesModel(Base):
    __tablename__ = "likes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey(
            "posts.id",
            ondelete="cascade",
        ),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


class PostsModel(Base):
    __tablename__ = "posts"

    __table_args__ = (
        Index(
            "idx_posts__text__title",
            *["text", "title"]
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow)

    text: Mapped[str]
    title: Mapped[str]
    tags: Mapped[list[str]] = mapped_column(
        ARRAY(String(64)),
        nullable=False,
        default=[],
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
        ),
        nullable=False,
    )
    likes_count: Mapped[int] = column_property(
        sa.select(sa.func.count(LikesModel.post_id))
        .where(LikesModel.post_id == id)
        .scalar_subquery()
    )

    author: Mapped["UsersModel"] = relationship(lazy="joined")
    likes: Mapped[List["LikesModel"]] = relationship()


class CommentsModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow)

    text: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey(
            "posts.id",
            ondelete="cascade",
        ),
        nullable=False,
    )
    author: Mapped["UsersModel"] = relationship(lazy="joined")
    post: Mapped["PostsModel"] = relationship(lazy="joined")

