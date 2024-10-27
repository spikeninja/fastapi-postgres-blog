from app.db.models import PostsModel
from app.schemas.posts import PostDTO, UserDTO


class PostMapper:
    @staticmethod
    def to_dto(post: PostsModel, is_liked: bool) -> PostDTO:
        """"""

        return PostDTO(
            id=post.id,
            created_at=post.created_at,
            updated_at=post.updated_at,
            text=post.text,
            title=post.title,
            tags=post.tags,
            is_liked=is_liked,
            user_id=post.user_id,
            likes_count=post.likes_count,
            author=UserDTO(
                id=post.author.id,
                name=post.author.name,
                email=post.author.email,
                created_at=post.author.created_at,
                updated_at=post.author.updated_at,
                deleted_at=post.author.deleted_at,
                hashed_password=post.author.hashed_password,
            )
        )

    @staticmethod
    def to_entity(dto: PostDTO) -> PostsModel:
        """"""
