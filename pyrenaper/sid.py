from collections import defaultdict
from typing import Optional, Dict, List
from .exceptions import *
from .settings import *
from PIL import Image
from io import BytesIO
import requests

class Sid:
    """Renaper SID API implementation.

    This class provides methods to access Argentina's Government ID validation Methods.
    User and password credentials should be obtained in RENAPER's panel: Administration -> API Key.
    """
    _token = None
    _env = None
    
    def __init__(self, env: str, username: str, password: str) -> None: 
        self._env = env
        self._credentials = {"username": username, 
                            "password": password}
        
    def build_url(self, url: str) -> str:
        """Contactenates domain url with current api request uris

        Args:
            url (str): desired endpoint

        Returns:
            str: final url
        """
        return ''.join((self._env['base_url'], url))
    
    def _get_auth_headers(self):
        return {"Authorization": " ".join(("Bearer", self._token))}        

            
    def _make_request(self, url: str, payload: dict=None, 
                      headers: dict=None, http_method: str='GET') -> Dict:
        
        try:
            if http_method == 'POST':
                request = requests.post(self.build_url(url),
                                        data=payload,
                                        headers=headers)
            else:
                request = requests.get(self.build_url(url),
                                       params = payload,
                                       headers=headers) 
        except Exception as e:
            raise e
        else:
            if request.status_code != 200:
                try:
                    return request.body
                except Exception as e:
                    raise e
                
            data = request.json()
            
            if 'data' in data:
                data = data['data']
        
            if data['codigo'] not in  [0, 99]:
                raise Exception(data.get('mensaje'))
        
        return data

    def login(self):
        self._token = self.get_token(self._credentials)
        
    def get_token(self, credentials) -> str:
        token_data = self._make_request("CHUTROFINAL/API_ABIS/Autorizacion/token.php",
                                        credentials, http_method='POST')
        return token_data['token']
        
        
    def get_basic_person_data(self, person_id: str, gender: str) -> Dict:
        params = {"dni": person_id, "sexo": gender}
        person_data = self._make_request("apidatos/porDniSexo.php",
                                params, http_method='GET',
                                headers=self._get_auth_headers())
        return person_data
    
    def get_full_person_data(self, person_id: str, gender: str, operation_id: str) -> Dict:
        params = {"dni": person_id, "sexo": gender, "idtramite": operation_id}
        person_data = self._make_request("apidatos/porDniSexoTramite.php",
                                params, http_method='GET',
                                headers=self._get_auth_headers())
        return person_data
    
    