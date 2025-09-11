import logging
from typing import Awaitable, Callable

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader, OpenIdConnect
from keycloak import KeycloakError, KeycloakOpenID

from app.config import settings
from app.models.rail_user import RailUser

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

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user_token(token=Security(oidc)):
    return token


def get_current_user_or_raise(
    from_token: bool = True, from_api_key: bool = False
) -> Callable[[str | None, str | None], Awaitable[dict]]:
    async def _get_current_user_or_raise(
        token: str | None = Security(oidc),
        api_key: str | None = Security(api_key_header),
    ) -> dict:
        user = await _get_user(from_token, from_api_key, token, api_key)
        if user is None:
            raise_requires_auth(
                "This endpoint requires authorization. You need to be logged in or provide an API key."
            )
        return user  # type: ignore[return-value]

    return _get_current_user_or_raise


def get_current_user_if_exists(
    from_token: bool = True, from_api_key: bool = False
) -> Callable[[str | None, str | None], Awaitable[dict | None]]:
    async def _get_current_user_if_exists(
        token: str | None = Security(oidc),
        api_key: str | None = Security(api_key_header),
    ) -> dict | None:
        return await _get_user(from_token, from_api_key, token, api_key)

    return _get_current_user_if_exists


async def _get_user(
    from_token: bool = True,
    from_api_key: bool = False,
    token: str | None = None,
    api_key: str | None = None,
) -> dict | None:
    if not from_token and not from_api_key:
        raise ValueError("Either from_token or from_api_key must be set to True")
    elif from_token and token:
        return await _get_userinfo(token)
    elif from_api_key and api_key:
        user_obj = await RailUser.find_one(RailUser.api_key == api_key)
        if user_obj is not None:
            return user_obj.to_dict()
        else:
            raise_requires_auth("Invalid API key")
    return None


async def is_admin(token: str | None = Security(oidc)) -> None:
    user_info = await _get_userinfo(token)

    if not has_admin_role(user_info):
        raise_requires_auth("You don't have enough privileges")


def has_admin_role(user_info: dict) -> bool:
    user_client_roles = (
        user_info.get("resource_access", {})
        .get(settings.AIOD_KEYCLOAK.CLIENT_ID, {})
        .get("roles", [])
    )
    return "admin_access" in user_client_roles


async def _get_userinfo(token: str | None) -> dict:
    if token is None:
        raise_requires_auth()
    else:
        token = token.replace("Bearer ", "")

    try:
        user_info = keycloak_openid.userinfo(token)
    except KeycloakError as e:
        _raise_invalid_token(e)

    return user_info


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
