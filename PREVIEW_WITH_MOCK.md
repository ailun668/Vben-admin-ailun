# 打包后预览（支持 Mock API）

## 问题

`pnpm preview`（Vite 预览服务器）是纯静态文件服务器，无法加载 mock 中间件。

## 解决方案

使用 **Express 服务器** 提供生产构建文件 + Mock API 支持。

---

## 使用步骤

### 1️⃣ 安装依赖

```bash
pnpm install
```

`express` 已自动添加到 `package.json`。

### 2️⃣ 构建应用

```bash
pnpm build
```

生成 `dist/` 目录的生产构建文件。

### 3️⃣ 启动预览服务器（支持 Mock API）

```bash
# 新增命令：使用 Express 服务器预览，支持 Mock API
pnpm preview:mock

# 或直接运行
node server.js
```

### 4️⃣ 访问应用

打开浏览器访问：**http://localhost:4176**

### 5️⃣ 测试登录

使用测试凭证登录：
- **用户名**: `admin`
- **密码**: `admin123`

或

- **用户名**: `user`
- **密码**: `user123`

---

## 对比

| 方式 | 命令 | Mock API | 适用场景 |
|------|------|----------|---------|
| 开发 | `pnpm dev` | ✅ 启用 | 开发和调试 |
| 预览（无 Mock） | `pnpm preview` | ❌ 禁用 | 检查构建大小 |
| **预览（有 Mock）** | `pnpm preview:mock` | ✅ 启用 | **推荐：测试打包后的完整功能** |

---

## server.js 说明

`server.js` 做了什么：

```javascript
// 1. 提供静态文件服务（dist 目录）
app.use(express.static(DIST_DIR));

// 2. 集成 Mock API（与开发环境一致）
app.post('/api/user/login', (req, res) => { ... });
app.get('/api/user/info', (req, res) => { ... });
app.post('/api/user/logout', (req, res) => { ... });
app.get('/api/user/list', (req, res) => { ... });

// 3. 处理 SPA 路由（Vue Router）
app.get('*', (req, res) => {
  res.sendFile(path.join(DIST_DIR, 'index.html'));
});
```

---

## 生产环境部署

当要部署到真实的生产环境时：

### 方案 A：使用 Express（推荐）

将 `server.js` 部署到服务器，配置真实 API：

```javascript
// 修改 server.js 中的 Mock API 路由
// 替换为调用真实后端的代码
app.post('/api/user/login', async (req, res) => {
  const response = await fetch('https://real-api.com/login', {
    method: 'POST',
    body: JSON.stringify(req.body)
  });
  res.json(await response.json());
});
```

或使用 `.env.production` 中配置的 API 地址。

### 方案 B：使用 Nginx

部署 `dist/` 到 Nginx，配置反向代理到真实后端：

```nginx
server {
    listen 80;
    root /var/www/dist;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend-server:3000;
    }
}
```

### 方案 C：使用云平台

- **Vercel**: 自动部署，配置环境变量
- **腾讯云/阿里云**: 部署 `dist/` 到静态网站托管，API 配置反向代理

---

## 故障排除

### Q: 启动 `pnpm preview:mock` 时报错？

**A**: 检查以下几点：

1. **Express 已安装**
   ```bash
   pnpm install  # 重新安装依赖
   ```

2. **已执行 build**
   ```bash
   pnpm build  # 生成 dist 目录
   ```

3. **检查端口是否被占用**
   ```bash
   # 修改端口
   PORT=5000 node server.js
   ```

### Q: 登录仍然失败？

**A**: 检查浏览器开发者工具 (F12) → Network 标签：

1. 查看 `/api/user/login` 请求的**状态码**
2. 查看**响应内容**是否包含 `token`
3. 如果显示 404，说明 server.js 没有正确启动

### Q: 静态文件加载失败？

**A**: 确保以下文件存在：

```bash
dist/
├── index.html
├── assets/
│   ├── *.css
│   └── *.js
└── ...
```

如果不存在，执行 `pnpm build`。

---

## 技术栈

- **框架**: Express.js
- **文件服务**: express.static
- **JSON 解析**: express.json/urlencoded
- **SPA 路由**: 自定义通配符路由

---

## 下一步

当你有真实的后端 API 时：

1. 修改 `.env.production` 配置 API 地址
2. 修改 `server.js` 中的 Mock API 为真实 API 调用
3. 或直接使用 `pnpm build && pnpm preview` 指向真实后端

