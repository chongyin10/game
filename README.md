# 游戏管理系统

这是一个游戏管理后端与前端项目，提供用户信息管理功能。

## 项目结构

```
game/
├── web/          # React + TypeScript 前端项目
└── py/           # Python Flask 后端项目
```

---

## Docker 部署

### 快速启动

1. **复制环境变量配置**

```bash
cp .env.example .env
```

2. **启动所有服务**

```bash
# 启动后端和数据库
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

服务启动后：
- 后端 API: `http://localhost:5002`
- PostgreSQL: `localhost:5432`

### Docker 常用命令

```bash
# 构建镜像
docker-compose build

# 启动服务（后台运行）
docker-compose up -d

# 启动服务（前台运行，查看日志）
docker-compose up

# 停止服务
docker-compose down

# 停止服务并删除数据卷
docker-compose down -v

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f backend
docker-compose logs -f postgres

# 进入容器
docker-compose exec backend bash
docker-compose exec postgres psql -U postgres -d game_db

# 重新构建并启动
docker-compose up -d --build
```

### 单独构建镜像

**后端镜像**

```bash
cd py
docker build -t game-backend .
docker run -p 5002:5002 --env-file ../.env game-backend
```

**前端镜像（待开发后使用）**

```bash
cd web
docker build -t game-frontend .
docker run -p 3000:80 game-frontend
```

### Docker 配置文件说明

| 文件 | 说明 |
|------|------|
| `docker-compose.yml` | Docker Compose 编排配置 |
| `py/Dockerfile` | Python Flask 后端镜像配置 |
| `py/.dockerignore` | 后端构建忽略文件 |
| `web/Dockerfile` | React 前端镜像配置 |
| `web/nginx.conf` | Nginx 配置文件 |
| `web/.dockerignore` | 前端构建忽略文件 |
| `init-db.sql` | 数据库初始化脚本 |
| `.env.example` | 环境变量示例 |

---

## 后端项目 (py/)

基于 Flask 的 RESTful API 服务，提供用户信息的增删改查功能。

### 技术栈

- **框架**: Flask 3.0.0
- **数据库**: PostgreSQL
- **数据库驱动**: psycopg2-binary 2.9.9
- **跨域支持**: flask-cors 4.0.0
- **环境配置**: python-dotenv 1.0.0

### 目录结构

```
py/
├── app.py              # Flask 应用入口
├── db_config.py        # 数据库连接配置
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量示例
├── core/               # 业务逻辑层
│   └── userinfo/       # 用户信息模块
└── routes/             # API 路由层
    └── userinfo_routes.py
```

### 快速开始

#### 1. 创建虚拟环境

```bash
cd py
python3 -m venv venv
```

#### 2. 激活虚拟环境

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置数据库

复制环境变量文件并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

#### 5. 启动服务

```bash
python app.py
```

服务将在 `http://127.0.0.1:5002` 启动。

### API 接口

#### 用户信息管理 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/userinfo/add` | POST | 添加用户 |
| `/api/userinfo/update` | PUT | 更新用户 |
| `/api/userinfo/delete` | DELETE | 删除用户 |
| `/api/userinfo/get` | GET | 获取单个用户 |
| `/api/userinfo/list` | GET | 获取用户列表 |

#### 接口详情

**添加用户**

```http
POST /api/userinfo/add
Content-Type: application/json

{
    "username": "张三",
    "email": "zhangsan@example.com",
    "phone": "13800138000",
    "password": "123456"
}
```

**更新用户**

```http
PUT /api/userinfo/update
Content-Type: application/json

{
    "user_id": 1,
    "username": "李四",
    "email": "lisi@example.com"
}
```

**删除用户**

```http
DELETE /api/userinfo/delete?user_id=1
```

**获取单个用户**

```http
GET /api/userinfo/get?user_id=1
GET /api/userinfo/get?email=zhangsan@example.com
GET /api/userinfo/get?phone=13800138000
GET /api/userinfo/get?username=张三
```

**获取用户列表**

```http
GET /api/userinfo/list?limit=100&offset=0
```

### 数据库操作

项目提供了 `Database` 类用于数据库操作：

```python
from db_config import Database

# 使用上下文管理器（推荐）
with Database() as db:
    # 查询数据
    result = db.execute_query("SELECT * FROM userinfo WHERE id = %s", (user_id,))
    
    # 插入/更新/删除数据
    db.execute_update("INSERT INTO userinfo (username) VALUES (%s)", ("张三",))
```

---

## 前端项目 (web/)

React + TypeScript + Vite 前端项目。

### 技术栈

- **框架**: React 18
- **语言**: TypeScript
- **构建工具**: Vite 5
- **路由**: React Router 6
- **HTTP 客户端**: Axios
- **代码规范**: ESLint

### 项目结构

```
web/
├── src/
│   ├── api/          # API 接口封装
│   ├── types/        # TypeScript 类型定义
│   ├── utils/        # 工具函数
│   ├── App.tsx       # 主组件
│   └── main.tsx      # 入口文件
├── public/           # 静态资源
├── index.html        # HTML 模板
├── vite.config.ts    # Vite 配置
└── tsconfig.json     # TypeScript 配置
```

### 快速开始

```bash
# 进入前端目录
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

开发服务器: `http://localhost:3000`

---

## 开发计划

- [ ] 完成前端 React + TypeScript 项目初始化
- [ ] 实现用户管理界面
- [ ] 添加游戏数据管理功能
- [ ] 集成前后端接口

---

## 许可证

MIT License
