from app.db.resources import AsyncSession
from app.repositories.users import UsersRepository
from app.repositories.posts import PostsRepository
from app.repositories.comments import CommentsRepository


class Repositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    def users(self) -> UsersRepository:
        return UsersRepository(session=self.session)

    def posts(self) -> PostsRepository:
        return PostsRepository(session=self.session)

    def comments(self) -> CommentsRepository:
        return CommentsRepository(session=self.session)
