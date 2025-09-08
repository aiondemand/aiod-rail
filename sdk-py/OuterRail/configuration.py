import jwt

from typing import Self
from datetime import datetime

from keycloak import KeycloakOpenID



class Configuration:
    """
    """

    def __init__(self,
                 host: str,
                 auth_host: str = "http://ec2-63-179-32-80.eu-central-1.compute.amazonaws.com/aiod-auth/",
                 auth_realm: str = "aiod",
                 auth_client_id: str = "outer-rail-sdk"
                 ) -> Self:
        self.host = host
        self.auth_client = KeycloakOpenID(server_url=auth_host, client_id=auth_client_id, realm_name=auth_realm)

    def login(self, username: str, password: str):
        response = self.auth_client.token(username=username, password=password, scope="openid profile email")
        self._update_from_response(response)

    def logout(self):
        self.auth_client.logout(self.refresh_token)
        self.expiration = None
        self.access_token = None
        self.refresh_token = None

    def _token(self) -> str:
        if self.expiration < datetime.now().timestamp():
            response = self.auth_client.token(self.refresh_token)
            return self._update_from_response(response)
        return self.access_token

    def _update_from_response(self, response) -> str:
        access_token = response.get("access_token")
        if access_token:
            payload = jwt.decode(access_token, options={"verify_signature": False})
            self.expiration = payload.get("exp") - 10
            self.access_token = access_token
            self.refresh_token = response.get("refresh_token")
        return access_token

    def _auth_settings(self, type: str) -> dict:
        auth = {}
        if type == "AccessToken":
            auth = {
                "type": "access_token",
                "in": "header",
                "key": "Authorization",
                "value": f"Bearer {self._token()}"
            }
        return auth
