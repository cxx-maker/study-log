
#Day19 · Git 分支 + CI

> 仓库：`https://github.com/cxx-maker/study-log`
> 今天做完的状态：`main` 有合并提交，GitHub Actions 出现第一个绿勾（`pytest #2`，17 秒）

---

## 一、分支：只是个指针

**分支不是复制一份文件。** 新建分支只是在 Git 内部多记一个“从这里开始”的标记，工作目录里的文件还是同一套，所以建分支零成本。

| 命令 | 干什么 |
|---|---|
| `git branch` | 列分支，`*` 是当前分支 |
| `git checkout -b 分支名` | 新建并立刻切过去（`git switch -c 分支名` 同义） |
| `git checkout 分支名` | 切到已有分支 |
| `git merge 分支名` | 把那个分支合到当前分支 |
| `git branch -d 分支名` | 删已合并的分支（没合并会拒绝，要强删才用 `-D`） |

命名习惯：正经开发用 `feature/xxx`、`fix/xxx`，临时实验用 `test/xxx`，一眼能看出用途。

---

## 二、制造并解决一次冲突

### 冲突怎么产生的

两个分支改了**同一个文件的同一行**，Git 不敢替你决定，就停下来问。

步骤（今天实际做的）：

```powershell
git checkout -b test/conflict
mkdir day19
Set-Content day19/conflict.txt "line A from branch" -Encoding utf8
git add .
git commit -m "conflict test from branch"

git checkout main
mkdir day19
Set-Content day19/conflict.txt "line A from main" -Encoding utf8
git add .
git commit -m "conflict test from main"

git merge test/conflict
```

合并时输出这段，**不是报错，是等你决定**：

```
CONFLICT (content): Merge conflict in day19/conflict.txt
Automatic merge failed; fix conflicts and then commit the result.
```

### 冲突标记怎么读

```
<<<<<<< HEAD
line A from main          ← 你当前分支的版本
=======
line A from branch        ← 要合进来的分支的版本
>>>>>>> test/conflict
```

### 解决三步

```powershell
# 1. 改文件：删掉三行标记，最终内容由你定（留一个、留两个、合着写都行）
Set-Content day19/conflict.txt "line A merged" -Encoding utf8

# 2. 告诉 git 这个文件我解决了
git add day19/conflict.txt

# 3. 完成本次合并
git commit -m "resolve conflict: merged line A"
```

**本质：合并结果由你决定，不是“选一个保留”。**

`git status` 里看到 `both added` 或 `both modified` 都按上面三步走，区别只在文件是两分支都新建的，还是两边都改过的。

想放弃这次合并：`git merge --abort`。

---

## 三、`git log --graph` 怎么读

```
* a223c3a (HEAD -> main) resolve conflict      ← 合并提交，有两个父
|\
| * 16ee337 (test/conflict) from branch        ← 分支上的提交
* | cae47d5 from main                          ← main 上的提交
|/
* 446db4b (origin/main) 学习linux的命令         ← 两条线的共同起点
```

`*` 一个提交，`|\` 从这里分出去，`| *` 右边那条（分支），`* |` 左边那条（main），`|/` 两条线合回来。**合并提交有两个父，普通提交只有一个**，所以它能把两条线接上。

---

## 四、CI：推上去自动跑测试

CI 一句话：**你把代码推上去，GitHub 自动开一台云机器，按你写的步骤跑一遍测试，绿勾或红叉告诉你结果。** 你电脑关着也照跑。所以 CI 里不能依赖本地 MySQL——那台机器上没有你的库。

### workflow 七个字段

```yaml
name: pytest              # 显示名，Actions 左侧栏就是它

on: push                  # 触发条件：推代码就跑

jobs:
  test:                   # 任务名，自己起
    runs-on: ubuntu-latest # 那台云机器用什么系统

    steps:                # 按顺序执行，某步失败后面不跑
      - uses: actions/checkout@v4        # 把仓库代码拉到机器上，不写这步上面什么都没有
      - uses: actions/setup-python@v5    # 装 Python
        with:
          python-version: "3.11"         # 和本地版本保持一致
      - run: pip install pytest          # run 就是执行命令
      - run: python -m pytest day19 -v
```

- 缩进**只用空格不用 Tab**，错一格整个文件就废
- `3.11` 的引号不能省，不加会被当成数字 `3.1`
- 想只在 main 上跑：`on: push` 换成

```yaml
on:
  push:
    branches: [main]
```

### 怎么判断 YAML 有没有读通

最实用的信号：**Actions 左侧栏显示的是 `pytest` 还是文件路径 `.github/workflows/test.yml`**。显示路径 = YAML 解析失败，job 也没正常跑。

### 从红到绿这一趟（面试素材）

第一次 `pytest #1` 红叉，`pytest #2` 绿勾，17 秒。中间三件事：

1. push 被拒：`refusing to allow a Personal Access Token to create or update workflow` —— token 缺 `workflow` scope
2. `test.yml` 改完没按 `Ctrl+S`，推上去的是空文件
3. 缩进修正后重新推，绿了

**面试怎么说（三句）**

> 我给自己的 study-log 仓库配了 GitHub Actions，推到 main 就自动拉起 Ubuntu 机器、装 Python 3.11、跑 pytest，全程 17 秒。
> 第一次跑是红的，workflow 文件缩进有问题，修完之后重新跑变绿，从红到绿整个闭环我自己走过一遍。
> 现在只跑了不依赖外部服务的用例，下一步用 `services` 起一个 MySQL 容器，把查库断言也纳入 CI。

这三句有动作、有失败、有修复、有后续计划，比背概念有力。

---

## 五、今天踩的五个坑

1. **PAT 缺 `workflow` scope**：GitHub 不让普通 token 改 `.github/workflows/`（CI 能执行任意命令、读密钥）。改 token 权限后还要去 **Windows 凭据管理器**删掉 `git:https://github.com` 的缓存，否则用的还是旧权限
2. **改完文件没保存**：VS Code 文件名旁有小圆点就是未保存，`Ctrl+S` 后圆点消失。没保存的改动 git 根本看不到
3. **YAML 缩进**：Tab 一律换成空格，VS Code 里 `Ctrl+Shift+P` → `Convert Indentation to Spaces`
4. **PowerShell 读 UTF-8 文件乱码**：`type README.md` 用 GBK 解码，中文会变乱码；正确写法 `Get-Content README.md -Encoding UTF8`
5. **`Set-Content -Encoding utf8` 会写 BOM**：文件开头多出看不见的字节，在 GBK 终端里显示成 `锘`。要无 BOM 用 `[System.IO.File]::WriteAllText(path, text, [System.Text.Encoding]::UTF8)`，或 PowerShell 7 的 `-Encoding utf8NoBOM`

---