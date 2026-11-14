from api.client import ApiClient

api = ApiClient("http://127.0.0.1:8000")
print("base_url=",repr(api.base_url))

r1 = api.get("/auth/me")
print("状态码:", r1.status_code)
print("响应体:", r1.json())

r2 = api.post("/auth/login",json={"username":"emilys","password":"emilyspass"})
token = r2.json()["accessToken"]
print("token长度：",len(token))

api.set_token(token)
print("Authorizatin:",api.session.headers["Authorization"][:30],"...")

r3 = api.get("/auth/me")
print("状态码:", r3.status_code)
print("响应体:", r3.json())