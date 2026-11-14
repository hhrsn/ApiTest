class AuthService:
    """认证相关接口：只管"怎么调"，不含任何断言"""

    def __init__(self, client):
        self.client = client

    def login(self, username, password):
        return self.client.post("/auth/login", json={"username": username, "password": password})

    def me(self):
        return self.client.get("/auth/me")
