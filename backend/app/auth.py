import logging
from typing import Awaitable, Callable

from fastapi import HTTPException, Security, status
from fastapi.security import OpenIdConnect
from keycloak import KeycloakError, KeycloakOpenID

from app.config import settings

oidc = OpenIdConnect(
    openIdConnectUrl=str(settings.AIOD_KEYCLOAK.OIDC_URL),
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


async def get_current_user_if_exists(token: str | None = Security(oidc)) -> dict | None:
    if token is None:
        return None

    token = token.replace("Bearer ", "")
    try:
        return keycloak_openid.userinfo(token)
    except KeycloakError as e:
        _raise_invalid_token(e)


async def get_current_user_or_raise(token: str | None = Security(oidc)) -> dict:
    user = await get_current_user_if_exists(token)
    if user is None:
        raise_requires_auth("This endpoint requires authorization. You need to be logged in or provide an API key.")
    return user  # type: ignore[return-value]


async def is_admin(token: str | None = Security(oidc)) -> None:
    user_info = await get_current_user_or_raise(token)
    if not has_admin_role(user_info):
        raise_requires_auth("You don't have enough privileges")


def has_admin_role(user_info: dict) -> bool:
    user_client_roles = (
        user_info.get("resource_access", {})
        .get(settings.AIOD_KEYCLOAK.CLIENT_ID, {})
        .get("roles", [])
    )
    return "admin_access" in user_client_roles


def raise_requires_auth(detail: str | None = None) -> None:
    if detail is None:
        detail = "This endpoint requires authorization. You need to be logged in."
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _raise_invalid_token(ex: KeycloakError) -> None:
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
