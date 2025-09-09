import jwt

from typing import Self
from datetime import datetime

from keycloak import KeycloakOpenID



class Configuration:
    """
    The configuration class servers for the setting up the SDK to work with external services.

    Any manager and most of the instances of the SDK need to be initialized with this class to work.

    Basic workflow when dealing with configuration would look as follows:

    1. Config has to be initialized with host url for the RAIL backend or optionally with other non-default constructor values.

    2. User needs to login to enable functionality that requires auth privileges.

    3. Instance of the config needs to be sent to managers that user wants to work with.

    >>> config = Configuration(host="https://rail.aiod.eu/api/docs") # 1
    >>> config.login(username="username", password="password") # 2
    >>> AssetManager(config) # 3
    """

    def __init__(self,
                 host: str,
                 auth_host: str = "http://ec2-63-179-32-80.eu-central-1.compute.amazonaws.com/aiod-auth/",
                 auth_realm: str = "aiod",
                 auth_client_id: str = "outer-rail-sdk"
                 ) -> Self:
        """
        Initializes a new Configuration.

        Args:
            host: (str): The url address that the SDK should connect to.
            auth_host: (str): Url of the keycloak server providing auth logic of the SDK.
            auth_realm: (str): The realm of the SSO for login.
            auth_client_id: (str): The client id of the SDK.

        Returns:
            Configuration: Initialized Configuration.

        Example:
            >>> Configuration(host="https://rail.aiod.eu/api/docs")
            Configuration
        """

        self.host = host
        self.auth_client = KeycloakOpenID(server_url=auth_host, client_id=auth_client_id, realm_name=auth_realm)

    def login(self, username: str, password: str):
        """
        Logs in the user with the given username and password.

        Args:
            username: (str): Username of the user in the RAIL service.
            password: (str): Password of the user in the RAIL service.

        Example:
            >>> config = Configuration(host="https://rail.aiod.eu/api/docs")
            >>> config.login(username="username", password="password")
            # User is logged in
        """

        response = self.auth_client.token(username=username, password=password, scope="openid profile email")
        self._update_from_response(response)

    def logout(self):
        """
        Logs out the currently logged in user.

        Example:
            >>> config = Configuration(host="https://rail.aiod.eu/api/docs")
            >>> config.login(username="username", password="password")
            >>> config.logout()
            # User is logged out
        """

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
