import json
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer,ThreadingHTTPServer

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE_DIR / "day17"))
from db import query

class handle(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def do_GET(self):
        if self.path =="/api/users":
            rows = query("SELECT username FROM users")
           # rows = [{"username": f"user{i:02d}", "age": 18, "city": "上海"} for i in range(1, 21)]

            body = json.dumps(rows,ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header("Content-Type","application/json;charset=utf-8")
            self.send_header("Content-Length", str(len(body)))

            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()
server = ThreadingHTTPServer(("127.0.0.1",8000),handle)
print("serving on 8000")
server.serve_forever()

