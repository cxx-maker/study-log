接口：POST /api/login
参数：username、password（都是 form 表单）
成功：200，返回 {"code": 0, "token": "xxx", "msg": "登录成功"}
失败：200，返回 {"code": 1001, "msg": "用户名或密码错误"}
业务规则：
  username 3-16 位，只能是字母数字下划线
  password 8-20 位，必须含字母和数字
  同一账号连续失败 5 次锁定 30 分钟
