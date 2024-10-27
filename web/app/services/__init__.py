from app.repositories import Repositories
from app.services.posts import PostsService


class Services:
    def __init__(self, repositories: Repositories):
        self.repositories = repositories

    def posts(self) -> PostsService:
        return PostsService(repositories=self.repositories)
