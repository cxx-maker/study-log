# Day 14 · SQL 基础

## 环境
MySQL 8.0.40 / Navicat 或 DBeaver / 库 testdb / 表 users（20 行）

## 建数据脚本
seed.sql：DROP → CREATE → INSERT 20 行，可重复执行，结果恒为 20 行。

## 四条语句

### 1. 全查
SELECT * FROM users;
→ 返回 20 行，所有列

### 2. 条件筛选
SELECT username, city FROM users WHERE age > 25;
→ 返回 6 行，只显示 username / city

### 3. 排序
SELECT username, age FROM users ORDER BY age DESC;
→ 返回 20 行，age 从大到小

### 4. 取前 N
SELECT username, age FROM users ORDER BY age DESC LIMIT 3;
→ 返回 3 行，年龄最大的 3 个

## 结论
- WHERE 筛行，SELECT 选列
- LIMIT 必须在 ORDER BY 后面（书写顺序固定）
- 执行顺序：FROM → WHERE → ORDER BY → LIMIT
- 数据脚本要幂等：DROP + CREATE + INSERT
