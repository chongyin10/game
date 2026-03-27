# Python PostgreSQL 开发环境

## 环境设置

### 1. 创建虚拟环境
```bash
python3 -m venv venv
```

### 2. 激活虚拟环境
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

## 数据库配置

1. 复制 `.env.example` 为 `.env`:
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的PostgreSQL数据库信息：
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

## 使用方法

### 基本用法
```python
from db_config import Database

# 使用上下文管理器（推荐）
with Database() as db:
    result = db.execute_query("SELECT * FROM your_table")
    for row in result:
        print(row)
```

### 执行查询
```python
# 查询数据
result = db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
```

### 执行更新
```python
# 插入数据
db.execute_update(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    ("张三", "zhangsan@example.com")
)

# 更新数据
db.execute_update(
    "UPDATE users SET name = %s WHERE id = %s",
    ("李四", user_id)
)

# 删除数据
db.execute_update("DELETE FROM users WHERE id = %s", (user_id,))
```

## 测试连接

运行以下命令测试数据库连接：
```bash
python db_config.py
```
