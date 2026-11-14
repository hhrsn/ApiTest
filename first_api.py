import requests

BASE_URL = "http://127.0.0.1:8000"

r = requests.get(f"{BASE_URL}/products/2")
body=r.json()

print("状态码:", r.status_code)
assert r.status_code == 20,f"价格不对，实际是 {body['price']}"
assert body["title"] == "测试商品 2"
assert body["price"] == 20
print("全部通过")
