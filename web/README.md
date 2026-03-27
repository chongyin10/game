# 游戏管理系统 - 前端

基于 React + TypeScript + Vite 构建的游戏管理系统前端项目。

## 技术栈

- **框架**: React 18
- **语言**: TypeScript
- **构建工具**: Vite 5
- **路由**: React Router 6
- **HTTP 客户端**: Axios
- **代码规范**: ESLint

## 项目结构

```
web/
├── public/             # 静态资源
├── src/
│   ├── api/           # API 接口
│   │   ├── userinfo.ts
│   │   └── index.ts
│   ├── types/         # TypeScript 类型定义
│   │   └── index.ts
│   ├── utils/         # 工具函数
│   │   └── request.ts # Axios 封装
│   ├── App.tsx        # 主组件
│   ├── App.css        # 主样式
│   ├── main.tsx       # 入口文件
│   └── index.css      # 全局样式
├── index.html         # HTML 模板
├── vite.config.ts     # Vite 配置
├── tsconfig.json      # TypeScript 配置
└── package.json       # 项目配置
```

## 快速开始

### 安装依赖

```bash
npm install
# 或
pnpm install
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

### 代码检查

```bash
npm run lint
```

### 类型检查

```bash
npm run type-check
```

## API 代理配置

开发环境已配置 API 代理，所有 `/api` 请求会自动转发到后端服务：

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5002',
      changeOrigin: true,
    },
  },
}
```

## 环境变量

创建 `.env.local` 文件配置环境变量：

```env
VITE_API_BASE_URL=/api
```

## Docker 部署

### 构建镜像

```bash
docker build -t game-frontend .
```

### 运行容器

```bash
docker run -p 3000:80 game-frontend
```

访问 http://localhost:3000

## 功能模块

### 用户管理

- 用户列表展示
- 用户信息查询
- 用户添加/编辑/删除

（更多功能开发中...）

## 开发规范

- 使用 TypeScript 编写代码
- 遵循 ESLint 规则
- 组件使用函数式组件 + Hooks
- 样式使用 CSS Modules 或普通 CSS

## 许可证

MIT License
