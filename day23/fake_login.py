import re

USERS = {
    "test01": "abc12345",
    "test_02": "def67890",
    "test03": "Abc12345",
}

def fake_login(username, password):
    # ① 校验 username：长度 + 字符集，一条正则搞定
    if not re.fullmatch(r"[A-Za-z0-9_]{3,16}", username):
        return {"code": 1002, "msg": "参数格式不合法"}

    if not (8 <= len(password) <= 20):
        return {"code": 1002, "msg": "参数格式不合法"}
    if not re.search(r"[A-Za-z]", password):
        return {"code": 1002, "msg": "参数格式不合法"}
    if not re.search(r"[0-9]", password):
        return {"code": 1002, "msg": "参数格式不合法"}

    # ③ 业务校验：用户不在表里，或密码对不上
    if username not in USERS or USERS[username] != password:
        return {"code": 1001, "msg": "用户名或密码错误"}

    return {"code": 0, "token": "fake-token-" + username, "msg": "登录成功"}
