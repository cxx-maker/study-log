import os
from pathlib import Path

import requests
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
print("读取的 .env:", env_path, "| 文件存在:", env_path.exists())

load_dotenv(env_path)
key = os.environ.get("DEEPSEEK_API_KEY")
if not key:
    raise SystemExit("DEEPSEEK_API_KEY 没读到")

print("key 长度:", len(key), "| 开头:", key[:8], "| 结尾:", key[-4:])

r = requests.get("https://api.deepseek.com/models",
                 headers={"Authorization": f"Bearer {key}"}, timeout=20)
print("models  ->", r.status_code)

r = requests.get("https://api.deepseek.com/user/balance",
                 headers={"Authorization": f"Bearer {key}"}, timeout=20)
print("balance ->", r.status_code, r.text[:150])
