"""
本地练习接口 —— 学接口测试用，不依赖外网，不依赖第三方库。

启动：python mock_api.py
地址：http://127.0.0.1:8000

这是一个给学习用的"假后端"：不连数据库，数据存在内存里，重启就还原。
接口的形状（字段名、状态码）都照着真实接口设计，所以以后换成真接口，代码基本不用改。
"""

import json
import re
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

# ---------- 内存里的假数据 ----------

PRODUCTS = [
    {
        "id": i,
        "title": f"测试商品 {i}",
        "price": i * 10,
        "category": "test",
        "stock": 100,
    }
    for i in range(1, 21)
]

TOKENS = {}          # token -> username
USERNAME = "emilys"
PASSWORD = "emilyspass"


# ---------- 请求处理 ----------

class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        # 每来一个请求打印一行，方便你亲眼看到"我的请求到了"
        print(f"  [收到] {self.command} {self.path}")

    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    # -------- GET --------

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/":
            return self._send(200, {
                "message": "本地练习接口已启动",
                "endpoints": [
                    "GET  /products?limit=10&skip=0",
                    "GET  /products/1",
                    "POST /auth/login   {\"username\":\"emilys\",\"password\":\"emilyspass\"}",
                    "GET  /auth/me      (需要请求头 Authorization: Bearer <token>)",
                    "POST /products     {\"title\":\"x\",\"price\":9}",
                    "GET  /status/500   任意状态码，用来练异常",
                    "GET  /delay/2      延时 2 秒，用来练超时",
                ],
            })

        if path == "/products":
            try:
                limit = int(query.get("limit", ["10"])[0])
                skip = int(query.get("skip", ["0"])[0])
            except ValueError:
                return self._send(400, {"message": "limit/skip must be integer"})
            if limit <= 0 or limit > 100:
                return self._send(400, {"message": "limit must be between 1 and 100"})
            if skip < 0:
                return self._send(400, {"message": "skip must be >= 0"})
            return self._send(200, {
                "products": PRODUCTS[skip: skip + limit],
                "total": len(PRODUCTS),
                "skip": skip,
                "limit": limit,
            })

        m = re.fullmatch(r"/products/(\d+)", path)
        if m:
            pid = int(m.group(1))
            for p in PRODUCTS:
                if p["id"] == pid:
                    return self._send(200, p)
            return self._send(404, {"message": f"Product with id '{pid}' not found"})

        if path == "/auth/me":
            auth = self.headers.get("Authorization")
            if not auth:
                return self._send(401, {"message": "Access Token is required"})
            if not auth.startswith("Bearer "):
                return self._send(401, {"message": "Invalid Authorization format"})
            token = auth.split(" ", 1)[1]
            if token not in TOKENS:
                return self._send(401, {"message": "Invalid token"})
            return self._send(200, {"username": TOKENS[token]})

        m = re.fullmatch(r"/status/(\d{3})", path)
        if m:
            code = int(m.group(1))
            if code < 200 or code > 599:
                return self._send(400, {"message": "status must be 200-599"})
            return self._send(code, {"message": f"forced status {code}"})

        m = re.fullmatch(r"/delay/(\d+)", path)
        if m:
            seconds = int(m.group(1))
            time.sleep(seconds)
            return self._send(200, {"slept": seconds})

        return self._send(404, {"message": f"no such route: {path}"})

    # -------- POST --------

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._read_body()
        if body is None:
            return self._send(400, {"message": "body must be valid JSON"})

        if path == "/auth/login":
            if body.get("username") != USERNAME or body.get("password") != PASSWORD:
                return self._send(400, {"message": "Invalid credentials"})
            token = uuid.uuid4().hex
            TOKENS[token] = body["username"]
            return self._send(200, {
                "accessToken": token,
                "refreshToken": token + "r",
                "username": body["username"],
                "email": "emily@example.com",
            })

        if path == "/products":
            if "title" not in body or "price" not in body:
                return self._send(400, {"message": "title and price are required"})
            if not isinstance(body["price"], int):
                return self._send(400, {"message": "price must be integer"})
            new = {
                "id": len(PRODUCTS) + 1,
                "title": body["title"],
                "price": body["price"],
                "category": "test",
                "stock": 0,
            }
            PRODUCTS.append(new)
            return self._send(201, new)

        return self._send(404, {"message": f"no such route: POST {path}"})


# ---------- 启动 ----------

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8000
    print("=" * 56)
    print(f"本地练习接口已启动：http://{HOST}:{PORT}")
    print(f"浏览器打开这个地址可以看到所有可用接口：http://{HOST}:{PORT}/")
    print("这个窗口不要关，关掉服务就停了。按 Ctrl+C 停止。")
    print("=" * 56)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
