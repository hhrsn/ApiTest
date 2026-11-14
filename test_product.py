import requests


BASE_URL = "http://127.0.0.1:8000"
def test_get_prodect_2():
    r = requests.get(f"{BASE_URL}/products/2")
    body=r.json()

    print("状态码:", r.status_code)
    assert r.status_code == 200
    assert body["title"] == "测试商品 2"
    assert body["price"] == 20
   
def test_get_product_not_exist():
    r = requests.get(f"{BASE_URL}/products/99999")
    assert r.status_code == 404
    assert r.json()["message"] == "Product with id '99999' not found"

def test_list_products_limit_zero():
    r = requests.get(f"{BASE_URL}/products",params={"limit":0})
    body = r.json()
    
    assert r.status_code == 400,f"期望400，实际{r.status_code}"
    assert body["message"] == "limit must be between 1 and 100",f"提示语不对，实际是 {body['message']}"