from utils.config import config

def test_login_success(auth_api):
    r = auth_api.login(config.API_USER,config.API_PASSWORD)
    
    body = r.json()
    assert r.status_code == 200,f"期望200,实际{r.status_code},响应：{r.text[:200]}"
    assert body["accessToken"],"响应里应该有accessToken"
    assert body["username"] == "emilys",f"用户名不对，实际是{body['username']}"
    
def test_me_without_token(auth_api):
    r = auth_api.me()
    
    assert r.status_code == 401,f"期望401，世实际{r.status_code}，响应：{r.text[:200]}"
    assert r.json()["message"] == "Access Token is required", \
        f"提示语不对，实际是 {r.json()['message']}"
        
def test_me_with_token(logged_in_auth):
    r = logged_in_auth.me()
    
    assert r.status_code == 200, f"期望 200，实际 {r.status_code}，响应：{r.text[:200]}"
    assert r.json()["username"] == "emilys", \
        f"应该返回 emilys，实际是 {r.json().get('username')}"