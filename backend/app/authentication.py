import logging

from fastapi import HTTPException, Security, status
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


def get_current_user(required: bool):
    async def _get_user(token: str = Security(oidc)) -> dict | None:
        if not required and not token:
            return None
        else:
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="This endpoint requires authorization. You need to be logged in.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return await _verify_token(token)

    return _get_user


async def _verify_token(token: str) -> dict:
    try:
        token = token.replace("Bearer ", "")
        return keycloak_openid.userinfo(token)  # perform a request to keycloak
    except KeycloakError as e:
        error_msg = e.error_message
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
