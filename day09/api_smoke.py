import time 
import requests
from read_config import load_config
cfg = load_config()
URL =cfg["BASE_URL"] + "/x/web-interface/nav"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
}

def main():
    start = time.time()
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=5)
    except requests.exceptions.Timeout:
        print("timeout: check your network")
        return
    except requests.exceptions.RequestException as e:
        print(f"request failed: {e}")
        return

    cost = (time.time() - start) * 1000
    print(f"status: {resp.status_code}")
    print(f"cost: {cost:.0f} ms")
    print(f"body: {resp.text[:200]}")

    data = resp.json()

    assert resp.status_code == 200, f"status is {resp.status_code}"
    assert data["code"] == -101, f"code is {data['code']}"
    assert data["data"]["isLogin"] is False, "isLogin is not False"

    print("all 3 assertions passed")

if __name__ == "__main__":
    main()