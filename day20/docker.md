# Day20 · Docker：用容器起数据库

> 环境：WSL（Ubuntu），Docker 29.1.3（apt 原生版）
> 产出：`d:\study-log\day20\seed.sql`（建表 + 20 行用户 + 12 条订单）

---

## 一、镜像 / 容器 / 数据：三层关系

| 层 | 是什么 | 会不会丢 |
|---|---|---|
| **镜像** `mysql:8.0` | 只读模板，含程序、依赖、默认配置，本身不能改 | 不会，永远在 |
| **容器** `mysql-test` | 镜像跑起来的实例，在镜像上加了一层**可写层** | 删容器就没了 |
| **数据** | 写在容器的可写层里 | 容器一删就全丢，除非用 volume |

两个类比：镜像像“安装包 / ISO”，容器像“已经装好并正在运行的系统”；面向对象里，镜像是类，容器是对象。

关键推论：

- 一个镜像可以跑出无数个容器，互相独立，所以 `--name` 不能重复
- `docker run` 跑几次就有几个容器
- **数据不能依赖容器存**，生产要挂 volume，测试要脚本化（seed.sql）

---

## 二、`docker run` 六个参数

```bash
docker run -d --name mysql-test \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=testdb \
  -p 3307:3306 \
  mysql:8.0
```

| 参数 | 作用 | 易错点 |
|---|---|---|
| `-d` | 后台运行 | 不加会占住终端 |
| `--name mysql-test` | 容器名，后续 logs/stop/rm 都用它 | 重名会冲突 |
| `-e MYSQL_ROOT_PASSWORD=...` | 环境变量，MySQL 首次启动必须给 root 密码 | 写成 `MYSQL_ROOTPASSWORD` 少下划线，镜像直接不认 |
| `-e MYSQL_DATABASE=testdb` | 启动时自动建库 | 只建库，不建表 |
| `-p 3307:3306` | **本机端口 : 容器内端口** | 顺序写反就连不上 |
| `mysql:8.0` | 镜像名:标签 | 不写标签默认 latest，版本会飘 |

`-p` 记法：**冒号左边是你从外面访问的端口，右边是容器里程序真正监听的端口。** 本地 3306 被 Windows 上的 MySQL 占了，所以用 3307。

---

## 三、容器管理六个命令

| 命令 | 作用 |
|---|---|
| `docker ps` | 只显示**正在运行**的容器 |
| `docker ps -a` | 显示**所有**容器，含已停止的 |
| `docker logs mysql-test --tail 20` | 看容器内部输出，排查唯一入口 |
| `docker stop mysql-test` | 优雅停止（容器还在，数据还在） |
| `docker start mysql-test` | 把停掉的容器重新点起来 |
| `docker rm -f mysql-test` | 删除容器，`-f` 表示运行中也强删，**数据一起没了** |

看日志的技巧：**从下往上读**，最后几行才是当前状态。看到 `/usr/sbin/mysqld: ready for connections` 才算真正能对外服务；上面那堆 `Creating database testdb` 是启动初期的记录。

`docker exec -it mysql-test mysql -uroot -p123456` 是进容器里执行命令，查库、跑 SQL 都用它。

---

## 四、今天的完整实战（面试素材）

### 起因

Day17 那套 pytest 连的是 Windows 本机 MySQL（3306）。现在换成一个干净容器（3307）。

### 第一步：换端口，撞红

`.env` 里 `DB_PORT=3307`，然后跑：

```
python -m pytest day17 -v
```

结果：

```
FAILED  test_db.py::test_users_count      pymysql.err.ProgrammingError: (1146, "Table...")
ERROR   test_order_fixture.py::...        pymysql.err.ProgrammingError: (1146, "Table...")
```

**注意这里报的是 1146 而不是 2003**：连接是通的，只是新库里没有表。

### 第二步：造数据

`day20\seed.sql` 里写 `DROP TABLE IF EXISTS` + `CREATE` + `INSERT`，然后导入：

```bash
docker exec -i mysql-test mysql -uroot -p123456 testdb < /mnt/d/study-log/day20/seed.sql
```

`-i` 必须有，`<` 是把文件内容喂给容器里的 mysql 客户端，最后的 `testdb` 指定导入哪个库。

### 第三步：同一套代码，绿了

```
2 passed in 0.34s
```

代码一行没改，`.env` 也没动，只把数据补齐了。

### 这条链说明了什么

**换了环境等于换了数据。** 本机能跑不代表别处能跑；数据不会自己跟过去，必须脚本化才能复现。

---

## 五、面试怎么讲（三句主答）

> 我给测试项目做了一次环境隔离验证：用例原来连本机 MySQL，我把库换成 Docker 容器、映射 3307，结果直接变红，报 1146 表不存在——说明我的测试依赖了本地那份数据。
> 我把建表和数据初始化写成 `seed.sql`，在新容器里一导，同一个用例就 `2 passed`，代码一行没改。
> 这件事让我确认测试能不能跑不能只看自己机器，所以接 GitHub Actions 时，我在 workflow 里起 MySQL、跑 seed、再跑 pytest，让 CI 和本地是同一套流程。

**三个必被追问**

- “直接把数据拷过去不行吗”：不行。容器无状态，拷一次只解决这一次，别人复现不了。数据必须脚本化、能进仓库、能被 CI 执行。
- “seed 跑两遍会重复吗”：会。所以用 `DROP TABLE IF EXISTS` + `CREATE`，或 `TRUNCATE`，保证幂等。
- “数据量很大怎么办”：seed 只造用例需要的最小数据集，别全量搬。大数据量走备份恢复或迁移工具，不塞进 CI。

---

## 六、今天踩的坑

1. `MYSQL_ROOTPASSWORD` 少一个下划线 → 镜像不认，用 `MYSQL_ROOT_PASSWORD`
2. `-e` 打成大写 `-E` → 报 `unknown shorthand flag: 'E' in -E`
3. 终端里 `Ctrl+V` 不粘贴，只插入字面 `^V` → 用鼠标右键或 `Ctrl+Shift+V`
4. WSL 的 `sudo service docker start` 报 `unrecognized service` → 改用 `sudo nohup dockerd > /tmp/dockerd.log 2>&1 &`
5. `docker ps` 是空的就以为容器没了 → 用 `docker ps -a`，停掉的还在

---