import requests

BASE_URL = "https://dummyjson.com"


def show(title, resp, keys=None):
    print("=" * 64)
    print(title)
    print("-" * 64)
    print("状态码       :", resp.status_code)
    print("Content-Type :", resp.headers.get("Content-Type"))
    body = resp.json()
    print("顶层字段     :", list(body.keys()))
    if keys:
        for k in keys:
            print(f"  {k:<12}:", body.get(k))
    print()


# 1) 列表：一次拿多条
r = requests.get(f"{BASE_URL}/products", params={"limit": 3}, timeout=10)
show("1. 商品列表 limit=3", r, keys=["total", "skip", "limit"])
print(">>> 这次实际拿到", len(r.json()["products"]), "条")
print(">>> 标题分别是:", [p["title"] for p in r.json()["products"]])
print()

# 2) 详情：拿一条
show("2. 商品详情 id=1",
     requests.get(f"{BASE_URL}/products/1", timeout=10),
     keys=["id", "title", "price", "category"])

# 3) 登录：拿 token
r = requests.post(f"{BASE_URL}/auth/login",
                  json={"username": "emilys", "password": "emilyspass"},
                  timeout=10)
show("3. 登录 emilys / emilyspass", r, keys=["username", "email"])
print(">>> accessToken 前 40 位:", r.json()["accessToken"][:40], "...")
print(">>> 完整 token 长度:", len(r.json()["accessToken"]), "字符")
print()

# 4) 不存在的资源：错误返回长什么样
show("4. 不存在的商品 id=99999",
     requests.get(f"{BASE_URL}/products/99999", timeout=10),
     keys=["message"])
