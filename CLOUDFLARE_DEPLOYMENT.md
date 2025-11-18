# Cloudflare Pages + Workers 完整部署指南

## 方案说明

- **Cloudflare Pages**: 托管前端应用（dist 文件）
- **Cloudflare Functions**: 提供 Mock API（自动部署）
- **API 集成**: Pages 自动路由 `/api/*` 请求到 Functions

---

## 部署步骤

### 步骤 1️⃣ 准备工作

#### 1.1 安装 Wrangler CLI（Cloudflare 官方工具）

```bash
npm install -g wrangler
# 或
pnpm add -g wrangler
```

#### 1.2 登录 Cloudflare

```bash
wrangler login
```

浏览器会打开 Cloudflare 登录页面，授权后返回终端。

#### 1.3 验证登录

```bash
wrangler whoami
```

应该显示你的 Cloudflare 账户信息。

---

### 步骤 2️⃣ 构建应用

```bash
pnpm install
pnpm build
```

生成 `dist/` 目录的生产构建文件。

---

### 步骤 3️⃣ 部署到 Cloudflare Pages

#### 方式 A：使用 GitHub 自动部署（推荐）

**3A-1: 推送代码到 GitHub**

```bash
git add .
git commit -m "chore: prepare for Cloudflare deployment"
git push origin main
```

**3A-2: 在 Cloudflare 中连接 GitHub**

1. 打开 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 进入 **Pages** → **连接 Git**
3. 授权 GitHub 账户
4. 选择你的仓库（学习/框架）
5. 配置构建设置：
   - **构建命令**: `pnpm build`
   - **输出目录**: `My enterprise/dist`
   - **Framework**: Vue

**3A-3: 自动部署**

代码推送时自动触发构建和部署。

---

#### 方式 B：手动部署（快速测试）

```bash
# 安装 Pages CLI
npm install -g wrangler

# 部署 dist 目录
wrangler pages deploy dist --project-name vben-admin-ailun
```

等待上传完成，会显示部署 URL。

---

### 步骤 4️⃣ 配置 API 域名

部署后，Cloudflare 会分配一个域名，例如：
```
https://vben-admin-ailun.pages.dev
```

**更新生产环境配置**：

编辑 `.env.production`：

```bash
VITE_API_BASE_URL=https://vben-admin-ailun.pages.dev/api
```

**重新构建并部署**：

```bash
pnpm build
wrangler pages deploy dist --project-name vben-admin-ailun
```

---

### 步骤 5️⃣ 验证部署

访问你的 Pages URL：

```
https://vben-admin-ailun.pages.dev
```

**测试登录**：

| 凭证 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | `admin` | `admin123` |
| 普通用户 | `user` | `user123` |

---

## 文件结构说明

```
My enterprise/
├── dist/                          # 构建输出（部署到 Pages）
├── functions/                     # Cloudflare Functions（自动部署）
│   └── api/user/
│       ├── login.js              # POST /api/user/login
│       ├── info.js               # GET /api/user/info
│       ├── logout.js             # POST /api/user/logout
│       └── list.js               # GET /api/user/list
├── wrangler.toml                 # Workers 配置（Pages Functions 使用）
├── .env.production               # 生产环境配置（API 地址）
└── CLOUDFLARE_DEPLOYMENT.md      # 本文件
```

---

## API 路由映射

| 请求 | 路径 | 处理函数 |
|------|------|---------|
| POST | `/api/user/login` | `functions/api/user/login.js` |
| GET | `/api/user/info` | `functions/api/user/info.js` |
| POST | `/api/user/logout` | `functions/api/user/logout.js` |
| GET | `/api/user/list` | `functions/api/user/list.js` |

---

## 常见问题

### Q: 部署后 API 请求返回 404？

**A**: 检查以下几点：

1. **确认 Functions 已部署**
   ```bash
   # 检查 functions 目录是否存在
   ls -la functions/
   ```

2. **API 地址是否正确**
   ```bash
   # 查看 .env.production
   cat .env.production
   ```

3. **清除浏览器缓存**
   - F12 → Application → Clear Site Data
   - 或无痕模式重新访问

4. **查看 Cloudflare 日志**
   - Cloudflare Dashboard → Pages → 项目 → Functions → Logs

### Q: 如何切换到真实后端 API？

**A**: 修改 `.env.production`：

```bash
# 原先的 Mock API
VITE_API_BASE_URL=https://vben-admin-ailun.pages.dev/api

# 修改为真实后端
VITE_API_BASE_URL=https://your-real-backend.com/api
```

重新构建并部署：
```bash
pnpm build
wrangler pages deploy dist --project-name vben-admin-ailun
```

### Q: 如何更新 Functions（API 逻辑）？

**A**: 修改 `functions/` 目录下的文件，然后重新部署：

```bash
git add .
git commit -m "update: api functions"
git push  # 自动部署（如果使用 GitHub 集成）
```

或手动部署：
```bash
wrangler pages deploy dist --project-name vben-admin-ailun
```

### Q: 支持自定义域名吗？

**A**: 支持。在 Cloudflare Dashboard 配置自定义域名：

1. Pages → 项目 → 设置 → 自定义域
2. 添加你的域名（需在 Cloudflare 托管）

示例：
```
https://admin.yourdomain.com
```

---

## 成本说明

| 服务 | 免费额度 | 价格 |
|------|---------|------|
| Pages | 无限构建、部署、存储 | 免费 |
| Functions | 100,000 请求/天 | 免费 |
| Workers | 100,000 请求/天 | 免费 |

> 💡 小型项目完全免费！

---

## 总结

```bash
# 一键部署流程
pnpm build                                    # 构建应用
wrangler pages deploy dist \
  --project-name vben-admin-ailun             # 部署到 Pages + Functions
```

访问：`https://vben-admin-ailun.pages.dev`

完成！现在你的应用已部署到 Cloudflare，Mock API 也能正常工作。🎉

