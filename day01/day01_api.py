import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

key = os.environ.get("DEEPSEEK_API_KEY")
if not key:
    raise SystemExit("DEEPSEEK_API_KEY 没读到：.env 里要有 DEEPSEEK_API_KEY=sk-xxx")

print("key 长度:", len(key), "| 前5位:", key[:5], "| 末4位:", key[-4:])

url = "https://api.deepseek.com/chat/completions"
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
payload = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "用一句话解释什么是 Python 虚拟环境"}],
}

resp = requests.post(url, headers=headers, json=payload, timeout=60)

print("HTTP", resp.status_code)
print("返回内容:", resp.text[:300])

resp.raise_for_status()
data = resp.json()
print(data["choices"][0]["message"]["content"])
print(data["usage"])
