import logging
import requests

logger = logging.getLogger(__name__)

class ApiClient:
    
    def __init__(self,base_url:str):
        self.base_url = base_url
        self.session = requests.Session()
        
    def request(self,method,path,**kwargs):
        url = self.base_url + path
        return self.session.request(method,url,timeout=10,**kwargs)
        
    def get(self,path,**kwargs):
        return self.request("GET",path, **kwargs)
    
    def post(self,path,**kwargs):
        return self.request("POST",path,**kwargs)
    
    def set_token(self,token):
        self.session.headers["Authorization"] = f"Bearer {token}"
    
        
    