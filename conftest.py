import pytest

from api.client import ApiClient
from services.auth_service import AuthService
from services.product_service import ProductService
from utils.config import config



@pytest.fixture

def api():
    return ApiClient(config.BASE_URL)

@pytest.fixture
def auth_api(api):
    return AuthService(api)

@pytest.fixture
def product_api(api):
    return ProductService(api)

_token_login_count = 0
@pytest.fixture(scope="session")
def token():
    global _token_login_count
    _token_login_count += 1
    print(f"\n>>> [token fixture] 第 {_token_login_count} 次登录")
    
    client = ApiClient(config.BASE_URL)
    resp = client.post("/auth/login", json={"username": config.API_USER, "password": config.API_PASSWORD})
    assert resp.status_code == 200,resp.text
    return resp.json()["accessToken"]

@pytest.fixture
def logged_in_api(api,token):
    "已带token的client"
    api.set_token(token)
    return api

@pytest.fixture
def logged_in_auth(api,token):
    """已带token的AuthService"""
    api.set_token(token)
    return AuthService(api)
