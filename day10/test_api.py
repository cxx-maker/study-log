import requests
from read_config import load_config

cfg = load_config()
URL = cfg["BASE_URL"] + "/x/web-interface/nav"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
}


def test_status_code_is_200():
    resp = requests.get(URL, headers=HEADERS, timeout=5)
    assert resp.status_code == 200


def test_business_code_is_minus_101():
    resp = requests.get(URL, headers=HEADERS, timeout=5)
    assert resp.json()["code"] == -101


def test_is_login_is_false():
    resp = requests.get(URL, headers=HEADERS, timeout=5)
    assert resp.json()["data"]["isLogin"] is False
