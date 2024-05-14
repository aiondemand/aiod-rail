from requests_oauthlib import OAuth2Session
import requests

class Authenticator:
    def __init__(self) -> None:
        self._openid_config = requests.get('https://aiod-dev.i3a.es/aiod-auth/realms/aiod/.well-known/openid-configuration').json()
        self._client_id = 'rail-public'
        self._redirect_uri = self._openid_config['authorization_endpoint']
        self._token_uri = self._openid_config['token_endpoint']
        self._session = self._create_session()
        self._response = None 

    @property
    def response(self):
        return self._response
    
    @property
    def client_id(self):
        return self._client_id
    
    def _create_session(self) -> OAuth2Session:
        return OAuth2Session(self._client_id, redirect_uri=self._redirect_uri)
    
    def get_access(self) -> dict:
        """
            Return header as a dictionary in form Authorization: "token_type access_token"
            @param: None
        """
        authorization_Url, _ = self._session.authorization_url(
            self._redirect_uri, 
            access_type="offline", 
            prompt="select_account"
        )
        print(f'\nPlease go to URL to authorize access: \n{authorization_Url}\n')
        authorization_response = input('\nEnter the full callback URL(will be generated in address bar): \n')
        self._response = self._session.fetch_token(
            self._token_uri,
            authorization_response=authorization_response
        )

        return {"Authorization" : f"{self._response['token_type']} {self._response['access_token']}"}