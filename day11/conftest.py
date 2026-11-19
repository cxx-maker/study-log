import requests
import pytest
from read_config import load_config

cfg = load_config()
URL = cfg["BASE_URL"] + "/x/web-interface/nav"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
}
@pytest.fixture(scope="session")
def nav():
    print("fixture 执行了")
    resp =requests.get(URL, headers=HEADERS, timeout=5)
    return resp
