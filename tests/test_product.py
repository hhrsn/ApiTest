import pytest


def test_list_products(product_api):
    r = product_api.list(limit=3)

    body = r.json()
    assert r.status_code == 200, f"期望 200，实际 {r.status_code}，响应：{r.text[:200]}"
    assert len(body["products"]) == 3, f"应该返回 3 条，实际 {len(body['products'])} 条"
    assert body["limit"] == 3
    assert body["skip"] == 0
    # 不断言 total == 20：其他用例会创建商品，总数会变
    assert body["total"] >= 3


def test_get_product_detail(product_api):
    r = product_api.get(1)

    body = r.json()
    assert r.status_code == 200
    assert body["id"] == 1, f"返回的 id 不对，实际 {body['id']}"
    assert body["title"], "标题不该为空"
    assert body["price"] > 0, f"价格应该是正数，实际 {body['price']}"


def test_get_product_not_exist(product_api):
    r = product_api.get(99999)

    assert r.status_code == 404, f"期望 404，实际 {r.status_code}"
    assert r.json()["message"] == "Product with id '99999' not found", \
        f"提示语不对，实际是 {r.json()['message']}"


@pytest.mark.parametrize("limit", [1, 5, 10], ids=["min", "mid", "max"])
def test_list_products_limit(product_api, limit):
    body = product_api.list(limit=limit).json()
    assert len(body["products"]) == limit


def test_list_products_limit_zero(product_api):
    r = product_api.list(limit=0)

    assert r.status_code == 400, f"期望 400，实际 {r.status_code}"
    assert r.json()["message"] == "limit must be between 1 and 100"


def test_create_product(product_api):
    r = product_api.create("接口测试商品", 88)

    body = r.json()
    assert r.status_code == 201, f"期望 201，实际 {r.status_code}，响应：{r.text[:200]}"
    assert body["title"] == "接口测试商品"
    assert body["price"] == 88
    assert body["id"] > 20, f"新商品的 id 应该大于 20，实际 {body['id']}"
