

def test_status_code_is_200(nav):
    assert nav.status_code == 200
def test_business_code_is_minus_101(nav):
    assert nav.json()["code"] == -101
def test_is_login_is_false(nav):
    assert nav.json()["data"]["isLogin"] is False
# def test_status_code_is_200():
#     resp = requests.get(URL, headers=HEADERS, timeout=5)
#     assert resp.status_code == 200


# def test_business_code_is_minus_101():
#     resp = requests.get(URL, headers=HEADERS, timeout=5)
#     assert resp.json()["code"] == -101


# def test_is_login_is_false():
#     resp = requests.get(URL, headers=HEADERS, timeout=5)
#     assert resp.json()["data"]["isLogin"] is False
