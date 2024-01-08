import logging

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OpenIdConnect
from keycloak import KeycloakError, KeycloakOpenID

from app.config import settings

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


async def get_current_user(token=Depends(get_current_user_token)) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint requires authorization. You need to be logged in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await _get_current_user(token)


# TODO find a better way how to have an optional authentication
# The only reason for implementing this optional auth is for one route to have
# two different behaviours based on whether the user is logged in or not...
async def get_current_user_optional(token=Depends(get_current_user_token)) -> dict:
    if not token:
        return {}
    return await _get_current_user(token)


async def _get_current_user(token: str):
    try:
        token = token.replace("Bearer ", "")
        return keycloak_openid.userinfo(token)  # perform a request to keycloak
    except KeycloakError as e:
        logging.error(f"Error while checking the access token: '{e}'")
        error_msg = e.error_message
        if isinstance(error_msg, bytes):
            error_msg = error_msg.decode("utf-8")
        detail = "Invalid authentication token"
        if error_msg != "":
            detail += f": '{error_msg}'"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
