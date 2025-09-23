import jwt
import time
import tomlkit
import requests
import datetime

from typing import Self
from pathlib import Path
from http import HTTPStatus

from keycloak import KeycloakOpenID, KeycloakPostError, KeycloakConnectionError

_user_token_file = Path("~/.aiod-rail/token.toml").expanduser()


def _datetime_utc_in(*, seconds: int) -> datetime.datetime:
    span = datetime.timedelta(seconds=seconds)
    return datetime.datetime.now(datetime.UTC) + span



class Token:
    """Ensures active access tokens provided through one dedicated refresh token."""

    def __init__(
            self,
            refresh_token: str,
            access_token: str | None = None,
            expires_in: int = -1,
            **_
    ):
        if expires_in > 0 and access_token is None:
            raise ValueError(
                "If `expires_in_seconds` is set, `access_token` must be set to a valid access_token"
            )
        self.refresh_token = refresh_token
        self.access_token = access_token or ""
        # Because of the minuscule time difference between the server sending the
        # response and us processing it, the `expires_in` may not be used directly
        # when calculating expiration time, therefore - 2 seconds.
        self._expiration_date = _datetime_utc_in(seconds=expires_in - 300 + 20)

    @property
    def has_expired(self) -> bool:
        return datetime.datetime.now(datetime.UTC) >= self._expiration_date

    @property
    def user_info(self) -> dict:
        return jwt.decode(self.access_token, options={"verify_signature": False})

    def __str__(self):
        return self.refresh_token

    def to_file(self) -> None:
        if not _user_token_file.exists():
            _user_token_file.parent.mkdir(parents=True, exist_ok=True)
            _user_token_file.touch()

        doc = tomlkit.document()
        doc.add("refresh_token", self.refresh_token)
        if not self.has_expired:
            doc.add("access_token", self.access_token)
            doc.add("expiration_date", self._expiration_date.isoformat())
        _user_token_file.write_text(tomlkit.dumps(doc))

    def invalidate(self) -> None:
        if _user_token_file.exists() and _user_token_file.is_file():
            open(_user_token_file, 'w').close()
        self.refresh_token = None
        self.access_token = None
        self._expiration_date = None

    @classmethod
    def from_file(cls) -> Self | None:
        file = _user_token_file
        if not file.exists() or not file.is_file() or file.stat().st_size == 0:
            return None

        doc = tomlkit.parse(_user_token_file.read_text())
        kwargs: dict[str, str | int] = {"refresh_token": str(doc["refresh_token"])}
        if "expiration_date" in doc:
            expiration_date = datetime.datetime.fromisoformat(doc["expiration_date"])
            expires_in = expiration_date - _datetime_utc_in(seconds=0)
            if expires_in.total_seconds() > 0:
                kwargs.update(
                    {
                        "access_token": str(doc["access_token"]),
                        "expires_in_seconds": expires_in.seconds,
                    }
                )
        return Token(**kwargs)  # type: ignore[arg-type]



class AuthenticationError(Exception):
    """Raised when an authentication error occurred."""



class Configuration:
    """
    Configuration class for the OuterRail SDK. Provides methods for specifying the host and handling authentication.
    """

    def __init__(self,
                 host: str,
                 auth_host: str = "https://auth.aiod.eu/aiod-auth/",
                 auth_realm: str = "aiod",
                 auth_client_id: str = "aiod-sdk",
                 login_timeout: int = 300
                 ) -> Self:
        """
        Initializes a new Configuration instance.

        Args:
            host: (str): The url address that the SDK should connect to.
            auth_host: (str): Url of the keycloak server providing auth logic of the SDK.
            auth_realm: (str): The realm of the SSO for login.
            auth_client_id: (str): The client id of the SDK.

        Returns:
            Configuration: Initialized SDK configuration.

        Example:
            >>> Configuration(host="https://rail.aiod.eu/api")
            Configuration
        """

        self.host = host
        self.login_timeout = login_timeout
        self.auth_client = KeycloakOpenID(server_url=auth_host, client_id=auth_client_id, realm_name=auth_realm)

    def login(self, persist: bool = False) -> None:
        """
        Get an API Key by prompting the user to log in through a browser.

        IMPORTANT: This is a blocking function, and will poll the authentication server until
        authentication is completed or `timeout_seconds` have passed.

        Args:
            persist (bool, optional): If set to true, the login session will persist between multiple executions of code
            in which case, login() doesn't need to be called every execution.
            In the background, the new api key (refresh token) will automatically be saved to the user
            configuration file (~/.aiod-rial/config.toml). Defaults to True.

        Raises:
            AuthenticationError: if authentication is unsuccessful in any way.

        Example:
            >>> config = Configuration(host="https://rail.aiod.eu/api")
            >>> config.login(persist=True)
            # User is logged in and token is persisted to file.

        Note:
            Implementations based on authentication in AIoD SDK:
            https://github.com/aiondemand/aiondemand/blob/develop/src/aiod/authentication/authentication.py
         """

        self.token_persist = persist
        persisted_token = Token.from_file()
        if persisted_token:
            self.token = persisted_token
            print("Using persisted token from file.")
            return

        self.token = self._login_sequence()
        if self.token_persist:
            self.token.to_file()
        print(f"Successfully logged in as: {self.token.user_info['email']}.")

    def logout(self) -> None:
        """
        Logouts the current user by invalidating the current token. Logout also erases the token persisted
        in a file created by login(persist=True).

        Raises:
            KeycloakPostError: if logout was unsuccessful.
            KeycloakConnectionError: if connection to auth server failed.

        Example:
            >>> config.logout()
            # User is logged out and the file containing the token is erased.
        """

        try:
            self.auth_client.logout(str(self.token))
            self.token.invalidate()
        except (KeycloakPostError, KeycloakConnectionError) as e:
                raise e
        finally:
            self.token = None

    def _login_sequence(self) -> Token:
        response = self.auth_client.device(scope="openid profile email")
        poll_interval = response["interval"]

        print("Please authenticate using one of two methods:\n")
        print(f"  1. Navigate to {response['verification_uri_complete']}")
        print(f"  2. Navigate to {response['verification_uri']} and enter code {response['user_code']}\n")
        print(f"This workflow will automatically abort after {self.login_timeout} seconds.")

        start_time = time.time()
        token_endpoint = self.auth_client.well_known()["token_endpoint"]
        self.auth_client.device()
        token_data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "client_id": self.auth_client.client_id,
            "device_code": response["device_code"],
        }
        # Poll the token endpoint until we get a response or timeout
        while time.time() - start_time < self.login_timeout:
            time.sleep(poll_interval)
            token_response = requests.post(token_endpoint, data=token_data)
            token_response_data = token_response.json()

            response = (token_response.status_code, token_response_data.get("error"))
            match response:
                case (HTTPStatus.OK, _):
                    self.auth_client.decode_token(token_response_data["access_token"], validate=True)
                    return Token(**token_response_data)
                case (HTTPStatus.BAD_REQUEST, "authorization_pending"):
                    continue
                case (HTTPStatus.BAD_REQUEST, "slow_down"):
                    poll_interval *= 1.5
                    continue
                case (HTTPStatus.BAD_REQUEST, "access_denied"):
                    raise AuthenticationError("Access denied by Keycloak server.")
                case (HTTPStatus.BAD_REQUEST, "expired_token"):
                    raise AuthenticationError("Device code has expired, please try again.")
                case (status, error):
                    raise AuthenticationError(
                        f"Unexpected error, please contact the developers ({status}, {error})."
                    )
        raise AuthenticationError(
            f"No successful authentication within {self.login_timeout} seconds."
        )

    def _refresh_token(self):
        try:
            token_response_data = self.auth_client.refresh_token(self.token.refresh_token)
        except KeycloakPostError:
            raise AuthenticationError("Refresh token is not valid. Use `aiod.create_token` to get a new one."
            ) from None
        except KeycloakConnectionError as e:
            e.add_note(f"Could not connect auth server, try again later.")
            raise

        self.auth_client.decode_token(token_response_data["access_token"], validate=True)
        return Token(**token_response_data)

    def _auth_settings(self, type: str) -> dict:
        if self.token.has_expired:
            try:
                self.token = self._refresh_token()
            except:
                print("Authentication token has expired, please log in again.")
                self.token = self._login_sequence()

        auth = {}
        if type == "AccessToken":
            auth = {
                "type": "access_token",
                "in": "header",
                "key": "Authorization",
                "value": f"Bearer {self.token.access_token}"
            }
        return auth
