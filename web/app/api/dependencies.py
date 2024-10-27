from typing import AsyncGenerator

from jwt.exceptions import PyJWTError
from fastapi import Depends, HTTPException, status, Header

from app.ioc import AppContainer, Scope
from app.repositories import Repositories
from app.core.security import decode_access_token, JWTBearer


async def get_repositories() -> AsyncGenerator[Repositories, None]:
    """"""

    async with AppContainer(scope=Scope.REQUEST) as container:
        yield await container.get(Repositories)


async def get_optional_user(
    authorization: str | None = Header(default=None),
    repositories: Repositories = Depends(get_repositories),
):
    """"""

    if not authorization:
        return None

    token = authorization.replace("Bearer ", "")

    try:
        payload = await decode_access_token(token=token)
    except PyJWTError:
        return None

    user_id = payload.get("sub", None)

    if not user_id:
        return None

    user = await repositories.users().get_by_id(_id=int(user_id))
    if not user:
        return None

    return user


async def get_current_user(
    token: str = Depends(JWTBearer()),
    repositories: Repositories = Depends(get_repositories)
):
    """Decodes JWT token and extracts user from db"""

    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials are not valid."
    )

    payload = await decode_access_token(token=token)

    user_id = payload.get("sub", None)

    if not user_id:
        raise cred_exception

    user = await repositories.users().get_by_id(_id=int(user_id))
    if not user:
        return cred_exception

    return user
