import logging

from fastapi import HTTPException, Security, status
from fastapi.security import OpenIdConnect
from keycloak import KeycloakError, KeycloakOpenID

from app.config import settings

oidc = OpenIdConnect(
    openIdConnectUrl="https://test.openml.org/aiod-auth/realms/dev/.well-known/openidx"
    "-configuration",
    auto_error=False,
)

keycloak_openid = KeycloakOpenID(
    server_url=settings.AIOD_KEYCLOAK.SERVER_URL,
    client_id=settings.AIOD_KEYCLOAK.CLIENT_ID,
    client_secret_key=settings.AIOD_KEYCLOAK.CLIENT_SECRET,
    realm_name=settings.AIOD_KEYCLOAK.REALM,
    verify=True,
)

KEYCLOAK_PUBLIC_KEY = (
    "-----BEGIN PUBLIC KEY-----\n"
    + keycloak_openid.public_key()
    + "\n-----END PUBLIC KEY-----"
)


# function for getting token from Keycloak by using keycloak_openid and client_credentials flow
def get_token():
    token = keycloak_openid.token(
        username=settings.AIOD_KEYCLOAK.CLIENT_ID,
        password=settings.AIOD_KEYCLOAK.CLIENT_SECRET,
        grant_type=["client_credentials"],
    )
    return token


async def get_current_user(token=Security(oidc)) -> dict:
    ctoken = keycloak_openid.get_token()
    print(ctoken)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint requires authorization. You need to be logged in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token = token.replace("Bearer ", "")
        token_info = keycloak_openid.decode_token(token, key=KEYCLOAK_PUBLIC_KEY)
        return token_info
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
