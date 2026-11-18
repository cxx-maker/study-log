# Day 7 · 接口测试 ②：环境变量 + 断言

> 日期：2026-11-18（周三）｜计划 100 分钟
> 目标：从「能发请求」升级到「让 Postman 自己判对错」

---

## 一、环境变量：为什么要有

### 问题

每条请求都要写一遍完整域名：

```
https://api.bilibili.com/x/web-interface/nav
https://api.bilibili.com/x/web-interface/suggest
https://api.bilibili.com/x/web-interface/ranking/v2
```

**改 5 条 = 改 5 遍**。换成测试环境那天，改到第 3 条就忘了前面改过没有。

### 解决

把公共部分抽成一个变量：

| Variable | Value |
|---|---|
| `base_url` | `https://api.bilibili.com` |

请求里写：

```
{{base_url}}/x/web-interface/nav
```

发送前 Postman 自动把 `{{base_url}}` 替换成域名。

### 价值有两层

1. **少写**：不用每条都重复那一长串
2. **少改**：域名、token 变了只改一行，几十条请求同时生效

### 三个坑

| 坑 | 现象 |
|---|---|
| 变量值填成完整 URL | `{{base_url}}/x/...` 变成重复路径，404 |
| 没保存（Ctrl+S） | 引用时取不到值 |
| 花括号用中文 `｛｝` | 变量不被识别，原样发出去 |

### 怎么判断环境有没有生效

- 右上角环境名高亮显示
- URL 里 `{{base_url}}` 显示成**带底色的小块**（已解析）
- 显示成**红色字** = 没选中环境或变量名写错

---

## 二、断言：让工具替你判对错

### 位置

`Scripts` 标签 → `After response`（有的版本叫 Post-response）

### 三条基础断言

```js
// 1. HTTP 状态码
pm.test("状态码是 200", function () {
    pm.response.to.have.status(200);
});

// 2. 业务状态码
pm.test("code 是 0", function () {
    pm.expect(pm.response.json().code).to.eql(0);
});

// 3. 字段结构
pm.test("data 是对象", function () {
    pm.expect(pm.response.json().data).to.be.an("object");
});
```

### 三条各管什么

| 断言 | 检查 | 失败说明 |
|---|---|---|
| 状态码 200 | 网络通讯通了 | 接口挂了、地址错了、被拦截 |
| `code = 0` | 业务处理成功 | 通讯通了但业务失败 |
| data 是对象 | 结构没变 | 后端改了返回结构 |

**这三条正好对应「双层状态」**：第一条管 HTTP 层，第二条管业务层，第三条管数据结构稳定性。

### 常用断言写法

```js
pm.expect(x).to.eql(0);          // 等于（严格比较）
pm.expect(x).to.be.a("number");  // 类型是数字
pm.expect(x).to.be.a("string");  // 类型是字符串
pm.expect(x).to.be.an("object"); // 类型是对象
pm.expect(x).to.have.lengthOf(3) // 数组长度
pm.expect(x).to.be.oneOf([0, 1]) // 属于某几个值之一
```

---

## 三、断言失败长什么样

故意把 `eql(0)` 改成 `eql(1)`，结果是 `2/3`：

```
PASSED  状态码是 200
FAILED  code 是 0 | AssertionError: expected +0 to deeply equal 1
PASSED  data 是对象
```

**读这行报错只看两处**：

- `expected +0` = 实际值
- `to deeply equal 1` = 期望值

也就是说：**实际返回 0，但我断言它该是 1**。

以后接口出问题，报错直接告诉你差在哪——是状态码不对、字段值不对，还是结构变了。这是人工肉眼看不到粒度的东西。

---

## 四、今天踩的四个真实坑

### 坑 1：浏览器能打开，Postman 返回 404

`jsonplaceholder.typicode.com/posts/1` 在浏览器正常返回 JSON，在 Postman 里 404（`{}`）。

从响应头读出来：`X-Powered-By: Express`、`Content-Length: 2`、`X-Ratelimit-Remaining: 3599999`——**请求确实到达了正确服务器**，只是路径没匹配上，大概率是复制时带进了不可见字符。

**教训**：URL 从浏览器复制容易带脏字符，必要时手动敲。

### 坑 2：返回 HTML 而不是 JSON = 被风控拦了

`/x/web-interface/nav` 在 Postman 里返回的不是 JSON 而是 HTML 错误页。

原因：Postman 默认不带浏览器 `User-Agent`，B 站认出来不是真人浏览器，直接拦掉。

**解决**：Headers 加两行

```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Referer: https://www.bilibili.com
```

**通用判断**：同样的地址浏览器能开、工具打不开，八成是少请求头。真实项目做接口测试，第一件事往往是把浏览器的那几个头抄过来。

### 坑 3：签名接口不能改参数

B 站的 `w_rid` 是根据**具体参数值**算出来的，`wts` 是时间戳。

- 改任意参数 → 签名对不上 → 请求被拒
- 放一段时间 → `wts` 过期 → 请求被拒

所以 B 站这类接口的完整 URL 相当于**一次性门票**，不能靠改路径批量造请求。

**这正是反爬虫的设计目的**：让你没法批量构造。

---

### 坑 4：你机器上的网络中间层会伪造响应

两个铁证：

- `jsonplaceholder.typicode.com/posts/1`：浏览器正常，Postman 返回 404 和 `{}`
- `api.github.com/users/this-user-does-not-exist`：返回 **200 OK**，而且 `login` 字段**把请求的名字原样回显**

GitHub 对不存在的用户**一定**返回 `404`，绝不会返回 200，更不会回显请求内容。

**结论**：这台机器访问境外 API 时，中间有代理 / VPN / 安全软件在接管，返回的是编造的数据。**境外 API 的响应在这台机器上不可信。**

**对策**：练接口用国内直连的站点（B 站），或公司内网服务。判断依据很简单——国内站点一切正常，一出境就出怪现象。

---

## 五、手敲 URL 为什么总是失败：改用 cURL 导入

### 手敲 URL 的三个死因

1. **缺请求头**：没有 `User-Agent`、`Referer`，被风控当成机器人，返回 HTML 错误页
2. **带脏字符**：从浏览器复制时夹进空格、`%20`、多余斜杠，界面上看不出来，服务器收到的是另一个地址
3. **签名参数改不了**：`w_rid` 按参数算、`wts` 有时效，改一下请求就作废

### 正解：Copy as cURL → Import

1. 浏览器 F12 → **Network** → 点 **Fetch/XHR** 过滤
2. 在任意一条 **200** 的请求上右键 → **Copy** → **Copy as cURL (bash)**
3. Postman 左上角 **Import** → 直接 Ctrl+V 粘贴 → **Continue** → **Import**
4. 自动生成完整请求，点 Send

**为什么可靠**：这是把浏览器**实际发出的那个请求原样导出**，`User-Agent`、`Referer`、`Cookie`、`w_rid`、`wts` 一个不少。浏览器里通的，导入后必然通。

**这是真实工作中最常用的技能**——测试人员的接口 90% 都是从浏览器这样搬进来的，没人手敲 URL。

### 今天的 5 条

| # | 接口 | 断言 | 结果 |
|---|---|---|---|
| 1 | `/x/web-interface/nav`（用户信息，未登录 `code: -101`） | 4 条 | 全过 |
| 2 | `/xlive/.../getMoreRecList`（直播推荐列表） | 5 条 | 全过 |
| 3-5 | 另外三条 B 站接口 | 通用模板 3 条 | 全过 |

### 通用模板（B 站接口通用）

```js
pm.test("状态码是 200", function () {
    pm.response.to.have.status(200);
});

pm.test("业务码是 0", function () {
    pm.expect(pm.response.json().code).to.eql(0);
});

pm.test("data 不为空", function () {
    pm.expect(pm.response.json().data).to.not.be.null;
});
```

**前提是响应格式统一**：B 站所有接口都是 `code / message / data` 三件套，所以同一套断言能批着用。这是自动化测试能成立的基础——格式不统一，几十个接口就得写几十套规则。

### 数组怎么断言

```js
// 是数组
pm.expect(pm.response.json().data.recommend_room_list).to.be.an("array");

// 不为空（防"格式对但没数据"）
pm.expect(pm.response.json().data.recommend_room_list).to.have.lengthOf.at.least(1);

// 取第一项里的字段
pm.expect(pm.response.json().data.recommend_room_list[0].roomid).to.be.a("number");
```

`[0]` 就是取数组第一项。这串写法和明天要写的 Python 代码几乎一模一样：

```python
data["recommend_room_list"][0]["roomid"]
```

---

## 六、弱断言 vs 强断言（今天最重要的一课）

### 弱断言：只验类型

```js
pm.expect(pm.response.json().login).to.be.a("string");
```

`octocat` 是字符串，`torvalds` 也是字符串，**测错了也不会红**。

### 强断言：验具体值

```js
pm.expect(pm.response.json().login).to.eql("torvalds");
```

实测：请求 `owner = this-user-does-not-exist`，断言写死 `eql("torvalds")`，立刻变红：

```
FAILED  login 是我请求的那个人 | AssertionError:
expected 'this-user-does-not-exist' to deeply equal 'torvalds'
```

### 结论

**断言只验类型，等于给假数据开绿灯。** 三条绿色不代表测对了，可能只是没测到。

这正是以后用 AI 生成用例时要防的「覆盖率虚高」——看着一大堆断言全绿，实际什么都没验证。

---

## 七、今日新词

| 词 | 一句话 |
|---|---|
| Environment | 环境变量集合，存域名、token 这类多接口共用的值 |
| `{{}}` | 变量引用的写法，发送前被替换成真实值 |
| `pm.test` | Postman 断言函数，第一个参数是这条检查的名字 |
| `pm.expect` | 断言主体，里面放「实际值 + 比较方式 + 期望值」 |
| After response | 请求完成后执行的脚本区，断言写这里 |
| Test Results | 断言结果面板，显示 PASSED / FAILED 和通过数 |
| User-Agent | 告诉服务器「我是什么客户端」，风控常看这个 |
| `X-Powered-By` | 响应头里暴露后端技术栈的字段（Express / PHP / ASP.NET） |
| Copy as cURL | 浏览器把一条请求连头带参数原样导出，粘进 Postman 直接能用 |
| Import | Postman 的导入入口，支持 cURL / JSON / 文件 |
| Path Variable | URL 里的 `:owner` 这种占位符，真值填在 Params 面板 |
| `[0]` | 取数组第一项，Postman 用点号、Python 用方括号，取的是同一样东西 |
| `lengthOf.at.least(1)` | 断言数组至少有 1 项，防「格式对但没数据」 |

---

## 八、今天的三个判定

1. **变量值只放公共部分**——域名放变量，路径留给请求
2. **断言至少写两条**——HTTP 层一条，业务层一条，只写一条等于没测
3. **返回 HTML 就是被拦了**——正常 API 返回 JSON，收到 HTML 说明根本没进业务逻辑
4. **断言必须落到具体值**——只验类型等于开绿灯，假数据照样全绿

---

## 九、一句话总结

**以前是你看结果，现在是机器看结果。**

断言不只是「自动检查」，它的真正价值是：**一次跑几十条，一条都不漏，错的那条还会告诉你错在哪。**