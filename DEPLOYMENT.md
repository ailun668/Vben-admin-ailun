# 部署指南

## 概述

本项目支持多环境部署，通过环境变量灵活切换开发和生产配置。

---

## 环境配置说明

### 开发环境 (Development)
- **文件**: `.env.development`
- **Mock API**: ✅ 启用
- **API 地址**: `/api`（相对路径，由 vite-plugin-mock 拦截）

```bash
pnpm dev  # 使用开发配置
```

### 生产环境 (Production)
- **文件**: `.env.production`
- **Mock API**: ❌ 禁用
- **API 地址**: 配置为真实后端服务器地址

---

## 部署步骤

### 步骤 1：配置生产 API 地址

编辑 `.env.production`，替换为你的真实后端 API 地址：

```bash
# .env.production
VITE_API_BASE_URL=https://your-api-server.com/api
VITE_ENV=production
```

**示例**：
```bash
# 阿里云
VITE_API_BASE_URL=https://api.example.com/api

# 本地服务器
VITE_API_BASE_URL=http://192.168.1.100:3000/api

# 相对路径（同域名）
VITE_API_BASE_URL=/api
```

### 步骤 2：构建生产版本

```bash
# 使用生产环境配置构建
pnpm build

# 输出到 dist 目录
# 此时 mock API 已禁用，所有请求将发送到生产 API 地址
```

### 步骤 3：部署到服务器

#### 方案 A：使用 Node.js 服务器（Express）

```bash
# 安装服务器依赖
npm install express

# 创建 server.js
```

```javascript
// server.js
const express = require('express');
const path = require('path');

const app = express();

// 静态文件服务
app.use(express.static(path.join(__dirname, 'dist')));

// 单页应用路由处理
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist/index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
```

启动服务器：
```bash
node server.js
# 访问 http://localhost:3000
```

#### 方案 B：使用 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/dist;
        try_files $uri $uri/ /index.html;
    }

    # 代理 API 请求到后端
    location /api/ {
        proxy_pass http://your-backend-server:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 方案 C：使用 Docker

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 步骤 4：验证部署

在生产环境中测试登录：
1. 访问 `https://your-domain.com`
2. 使用后端提供的凭证登录
3. 检查浏览器开发者工具 → Network，确认 API 请求发送到正确的后端地址

---

## 常见问题

### Q: 部署后无法登录？

**A**: 检查以下几点：

1. **验证 API 地址**
   ```bash
   # 检查构建时的环境变量
   grep VITE_API_BASE_URL .env.production
   ```

2. **检查网络请求**
   - 打开浏览器开发者工具 (F12)
   - 点击登录，查看 Network 标签
   - 检查 `/api/user/login` 请求的状态和响应

3. **检查后端服务**
   - 确保后端 API 服务正在运行
   - 检查后端日志中是否有错误

4. **检查 CORS**
   - 如果前后端域名不同，需要配置 CORS
   ```javascript
   // 后端 Express 示例
   app.use(cors({
     origin: 'https://your-frontend-domain.com',
     credentials: true
   }));
   ```

### Q: 如何在生产环境中保留 mock API（仅测试用）？

**A**: 编辑 `vite.config.ts`，将 `prodEnabled` 改为 `true`：

```typescript
viteMockServe({
  mockPath: 'src/mock',
  enable: true,
  localEnabled: isDev,
  prodEnabled: true  // ⚠️ 仅用于测试，生产应设为 false
})
```

> ⚠️ **警告**: 生产环境使用 mock 数据是不安全的，仅用于演示和测试！

### Q: 如何快速切换 API 地址？

**A**: 创建不同的环境配置文件：

```bash
.env.development      # 开发环境
.env.production       # 生产环境
.env.staging          # 测试环境
```

然后构建时指定环境：
```bash
pnpm build --mode staging  # 使用 .env.staging
```

---

## 相关文件说明

| 文件 | 说明 |
|------|------|
| `.env.development` | 开发环境配置（启用 mock） |
| `.env.production` | 生产环境配置（使用真实 API） |
| `vite.config.ts` | Vite 配置（根据环境启用/禁用 mock） |
| `src/api/http.ts` | HTTP 客户端（自动使用环境变量配置的 API 地址） |
| `src/api/user.ts` | 用户 API 接口 |

---

## 总结

| 环境 | Mock API | API 地址配置 | 命令 |
|------|----------|------------|------|
| 开发 | ✅ 启用 | `.env.development` | `pnpm dev` |
| 生产 | ❌ 禁用 | `.env.production` | `pnpm build` |

开发时使用 mock API 快速开发，部署时配置真实后端地址。简单高效！

