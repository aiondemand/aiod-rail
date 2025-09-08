import logging
from typing import Awaitable, Callable

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader, OpenIdConnect
from keycloak import KeycloakError, KeycloakOpenID

from app.config import settings
from app.models.rail_user import RailUser

oidc = OpenIdConnect(
    openIdConnectUrl=settings.AIOD_KEYCLOAK.OIDC_URL,
    auto_error=False,
)

keycloak_openid = KeycloakOpenID(
    server_url=settings.AIOD_KEYCLOAK.SERVER_URL,
    client_id=settings.AIOD_KEYCLOAK.CLIENT_ID,
    client_secret_key=settings.AIOD_KEYCLOAK.CLIENT_SECRET,
    realm_name=settings.AIOD_KEYCLOAK.REALM,
    verify=True,
)


async def get_current_user_token(token=Security(oidc)):
    return token


def get_current_user(
    required: bool,
) -> Callable[[str | None, str | None], Awaitable[dict | None]]:
    """
    Get the current user based on the token provided in the header (returns an async function).

    Args:
        required (bool): Whether the user is required to be authenticated.
        from_token (bool): Whether the user can be authenticated through OIDC.
    """

    async def _get_user(token: str = Security(oidc)) -> dict | None:
        """
        Get the current user based on the provided token

        Args:
            token (str): The token provided by the user.
        """
        if not required and not token:
            return None
        elif token:
            return await _get_userinfo(token)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This endpoint requires authorization. You need to be logged in or provide an API key.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return _get_user


async def is_admin(token: str = Security(oidc)):
    user_info = await _get_userinfo(token)

    if not has_admin_role(user_info):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough privileges",
            headers={"WWW-Authenticate": "Bearer"},
        )


def has_admin_role(user_info: dict) -> bool:
    user_client_roles = (
        user_info.get("resource_access", {})
        .get(settings.AIOD_KEYCLOAK.CLIENT_ID, {})
        .get("roles", [])
    )
    return "admin_access" in user_client_roles


async def _get_userinfo(token: str) -> dict:
    if token is None:
        raise_requires_auth()

    token = token.replace("Bearer ", "")

    try:
        return keycloak_openid.userinfo(token)
    except KeycloakError as e:
        _raise_invalid_token(e)


def raise_requires_auth():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="This endpoint requires authorization. You need to be logged in.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _raise_invalid_token(ex: KeycloakError):
    error_msg = ex.error_message
    error_detail = "Invalid authentication token"

    if isinstance(error_msg, bytes):
        error_msg = error_msg.decode("utf-8")

    if error_msg:
        error_detail = f"{error_detail}: '{error_msg}'"

    logging.error(error_detail)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error_detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
