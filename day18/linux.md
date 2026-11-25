# Day18 · Linux 与日志

> 环境：WSL（Ubuntu），`root1@CHENXIXI`
> 路径对照：Windows 的 `d:\study-log` 在 WSL 里是 `/mnt/d/study-log`

---

## 一、必会 10 个命令

| 命令 | 干什么 | 最常用参数 | 例子 |
|---|---|---|---|
| `pwd` | 打印当前所在目录（绝对路径） | 无 | `pwd` |
| `cd` | 切换目录 | `..` 上一级、`~` 回家、`-` 回上一个目录 | `cd ..` / `cd ~` / `cd -` |
| `ls` | 列目录内容 | `-l` 详细、`-a` 含隐藏、`-h` 可读大小 | `ls -lah` |
| `cat` | 一次打印整个文件 | `-n` 带行号 | `cat -n app.log` |
| `grep` | 按内容筛行 | `-n` 行号、`-i` 忽略大小写、`-C N` 上下文、`-c` 只数条数、`-v` 反向 | `grep -in "error" app.log -C 3` |
| `tail` | 看文件末尾 | `-n 20` 最后 20 行、`-f` 实时跟随 | `tail -f app.log` |
| `ps` | 查进程 | `aux` 全部进程 | `ps aux \| grep sleep` |
| `kill` | 结束进程 | 默认 SIGTERM（礼貌）、`-9` 强杀 | `kill 67` / `kill -9 67` |
| `chmod` | 改权限 | 数字法 755/644、符号法 `+x` | `chmod 755 run.sh` |
| `df` | 查磁盘空间 | `-h` 人类可读 | `df -h` |

补充两个统计用的：`wc -l` 数行数、`awk '{print $N}'` 取第 N 列。

---

## 二、路径：绝对 vs 相对

- **`/` 开头 = 绝对路径**，从根算起：`cd /mnt/d/study-log/day18`
- **不带 `/` = 相对路径**，从当前位置往后找：`cd day18`

报 `No such file or directory` 时先查两件事：路径开头有没有 `/`、`pwd` 是不是你以为的位置。这两个原因占九成。

---

## 三、权限：那一串 `drwxr-xr-x` 怎么读

```
d  rwx  r-x  r-x
│   │    │    │
│   │    │    └ others：读 + 执行
│   │    └ group：读 + 执行
│   └ owner：读 + 写 + 执行
└ 类型：d 目录 / - 普通文件 / l 链接
```

`r`=4、`w`=2、`x`=1，三个加起来就是 chmod 用的那个数：

| 数字 | 权限 | 常见用途 |
|---|---|---|
| 755 | rwxr-xr-x | 目录、可执行脚本 |
| 644 | rw-r--r-- | 普通文件（只有自己能改） |
| 777 | rwxrwxrwx | 全开，一般不推荐 |

两种改法：数字法 `chmod 755 文件`；符号法 `chmod +x 文件`（给所有者、同组、其他人全加执行权）。

---

## 四、`./run.sh` 和 `bash run.sh` 的区别

`bash` 是命令解释器，你敲的每条命令都是它在解析执行，脚本第一行 `#!/bin/bash` 就是指定用谁来跑。

| 写法 | 本质 | 需要什么权限 |
|---|---|---|
| `./run.sh` | 把脚本当**可执行程序**启动 | 需要 `x` |
| `bash run.sh` | 把脚本当**文本参数**喂给 bash | 只要 `r` |

一句话：**前者需要你能执行这个文件，后者只需要你能读这个文件。**

---

## 五、日志排查三步（面试原题）

```bash
tail -n 100 app.log                      # 1. 先看最近 100 行发生了什么
grep -in "error" app.log -C 3            # 2. 定位错误，带行号 + 上下 3 行
awk '{print $3}' app.log | sort | uniq -c # 3. 统计各级别各多少条
```

- `grep -C 3` 的上下文是排查的关键，只看一行 ERROR 判断不了原因
- `uniq -c` 按**原文**计数，`ERROR` 和 `error` 会分成两行；要合并先转大小写：`awk '{print toupper($3)}' app.log | sort | uniq -c`
- 实时盯错误：`tail -f app.log | grep -i error`，另开一个窗口 `echo "... ERROR ..." >> app.log` 立刻就能看到跳出来

`/var/log` 里几个常打交道的：`syslog` 系统总日志、`auth.log` 登录认证、`dpkg.log` 装包记录、`kern.log` 内核。

---

## 六、今天踩的四个坑

1. `cd mnt/d/...` 少了开头 `/`，报 `No such file or directory` —— 相对路径从当前位置算
2. `/mnt/d` 下的文件 `chmod` 无效，永远显示 `-rwxrwxrwx` —— WSL 挂载 Windows 盘不保留 Linux 权限位，要到 `~` 里才测得出来
3. `ps aux | grep sleep` 会多出一行 `grep --color=auto sleep`，那是 grep 自己 —— 用 `grep "[s]leep"` 或 `grep -v grep` 排掉
4. 对比 `grep -n` 和 `grep -i -C 2` 时拿 `tail` 去比了 —— 对比实验要先确认比的是哪两条

---

## 七、自检

1. `cd -` 和 `cd ..` 各回哪里？
2. `755` 拆成 rwx 是什么？为什么目录常用 755、文件常用 644？
3. 权限只有 `r` 没有 `x` 的时候，`./run.sh` 和 `bash run.sh` 哪个能跑？
4. 统计日志里 error 一共多少条，写出完整命令。
5. 服务突然挂了，第一眼用哪个命令确认磁盘没满？

---