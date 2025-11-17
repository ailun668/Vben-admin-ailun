# 部署验证清单

## 环境对比

```
┌─────────────────────────────────────────────────────────┐
│           环境配置对比                                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  开发环境 (pnpm dev)                                     │
│  ├─ 基础地址: http://localhost:5173                     │
│  ├─ API 地址: http://localhost:5173/api                │
│  ├─ 登录接口: POST /api/user/login                      │
│  └─ Mock API: vite-plugin-mock (开发服务器)             │
│                                                           │
│  本地预览 (pnpm preview:mock)                            │
│  ├─ 基础地址: http://localhost:4176                     │
│  ├─ API 地址: http://localhost:4176/api                │
│  ├─ 登录接口: POST /api/user/login                      │
│  └─ Mock API: Express 服务器                             │
│                                                           │
│  ✅ 部署生产 (Cloudflare Pages)                          │
│  ├─ 基础地址: https://vben-admin-ailun.pages.dev       │
│  ├─ API 地址: https://vben-admin-ailun.pages.dev/api   │
│  ├─ 登录接口: POST /api/user/login                      │
│  └─ Mock API: Cloudflare Functions                       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 部署前检查

### ✅ 代码准备

```bash
# 检查所有文件已保存
git status

# 查看 .env.production 配置
cat .env.production
```

应该显示：
```
VITE_API_BASE_URL=https://vben-admin-ailun.pages.dev/api
```

### ✅ 构建验证

```bash
# 清理旧构建
rm -rf dist/

# 构建应用
pnpm build

# 验证构建结果
ls -la dist/
```

应该包含：
- `index.html`
- `assets/` 目录
- 其他资源文件

### ✅ 本地测试

```bash
# 测试预览服务器（可选）
pnpm preview:mock

# 访问：http://localhost:4176
# 测试登录：admin / admin123
```

---

## 🌐 部署到 Cloudflare Pages

### 方式 A：自动部署（推荐）

**第 1 步：推送代码到 GitHub**

```bash
git add .
git commit -m "chore: configure Cloudflare Pages deployment"
git push origin main
```

**第 2 步：在 Cloudflare 中连接 GitHub**

1. 访问 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 进入 Pages 项目 → **连接 Git**
3. 选择仓库：`学习/框架`
4. 配置构建设置：
   - **Root directory**: `my-vue-app`
   - **Build command**: `pnpm build`
   - **Build output directory**: `dist`

**第 3 步：监控部署**

- Cloudflare 自动开始构建
- 等待部署完成（2-5 分钟）
- 访问 `https://vben-admin-ailun.pages.dev`

---

### 方式 B：手动部署（快速测试）

```bash
# 安装 Wrangler（如未安装）
npm install -g wrangler

# 登录 Cloudflare
wrangler login

# 部署 dist 目录
wrangler pages deploy dist --project-name vben-admin-ailun
```

---

## ✅ 部署后验证

### 1️⃣ 访问应用

打开浏览器访问：
```
https://vben-admin-ailun.pages.dev
```

应该看到登录页面。

### 2️⃣ 测试登录

**测试账户 1：管理员**
```
用户名: admin
密码: admin123
```

**测试账户 2：普通用户**
```
用户名: user
密码: user123
```

### 3️⃣ 检查 Network 请求

打开浏览器开发者工具 (F12) → **Network** 标签

**登录时应该看到**：

| 请求 | 方法 | URL | 状态 |
|------|------|-----|------|
| user/login | POST | `https://vben-admin-ailun.pages.dev/api/user/login` | 200 ✅ |
| user/info | GET | `https://vben-admin-ailun.pages.dev/api/user/info` | 200 ✅ |

### 4️⃣ 检查响应数据

点击登录请求 → **Response** 标签，应该看到：

```json
{
  "code": 0,
  "data": {
    "token": "admin_token_12345",
    "user": {
      "id": "1",
      "username": "admin",
      "realName": "管理员",
      "roles": ["admin"],
      "permissions": [...]
    }
  },
  "message": "登录成功"
}
```

### 5️⃣ 功能验证

| 功能 | 操作 | 预期结果 |
|------|------|---------|
| 登录 | 输入正确凭证 | ✅ 进入首页 |
| 侧边栏 | 登录后检查菜单 | ✅ 显示可访问的菜单项 |
| 系统日志 | 点击系统日志菜单 | ✅ 显示日志列表 |
| 用户管理 | 点击用户管理菜单 | ✅ 显示用户列表 |
| 登出 | 点击登出按钮 | ✅ 返回登录页 |

---

## 🔧 故障排除

### 问题 1：部署后显示 404

**可能原因**：
- [ ] `dist/` 目录为空
- [ ] 构建命令配置错误
- [ ] 输出目录配置错误

**解决方案**：
```bash
# 重新构建
pnpm build

# 验证 dist 存在
ls dist/index.html

# 重新部署
wrangler pages deploy dist --project-name vben-admin-ailun
```

### 问题 2：API 请求返回 404

**可能原因**：
- [ ] API 地址配置错误（.env.production）
- [ ] Functions 文件未部署
- [ ] CORS 配置问题

**解决方案**：
```bash
# 检查 .env.production
cat .env.production | grep VITE_API_BASE_URL

# 应该显示：
# VITE_API_BASE_URL=https://vben-admin-ailun.pages.dev/api

# 检查 Functions 是否存在
ls -la functions/api/user/
```

### 问题 3：登录失败

**可能原因**：
- [ ] 输入的凭证错误
- [ ] API 响应格式不匹配
- [ ] Token 未正确保存

**解决方案**：
1. 打开浏览器 DevTools (F12)
2. 切换到 **Console** 标签
3. 查看错误信息
4. 检查 **Network** 标签中的 API 响应

---

## 📝 部署验证清单

在部署前，请完成以下检查：

- [ ] `.env.production` 配置正确
  ```bash
  grep VITE_API_BASE_URL .env.production
  ```

- [ ] `dist/` 目录存在且不为空
  ```bash
  ls -la dist/ | head -20
  ```

- [ ] `functions/` 目录中有 4 个 API 文件
  ```bash
  ls functions/api/user/
  ```

- [ ] 本地预览测试通过
  ```bash
  pnpm preview:mock
  # 访问 http://localhost:4176
  # 测试登录
  ```

- [ ] Git 代码已提交
  ```bash
  git status  # 应该是 clean
  ```

---

## 🎯 部署命令总结

```bash
# 完整部署流程（一条命令）
pnpm build && \
wrangler pages deploy dist --project-name vben-admin-ailun

# 或分步执行
pnpm build                    # 第 1 步：构建应用
wrangler pages deploy dist \  # 第 2 步：部署到 Pages
  --project-name vben-admin-ailun
```

---

## ✅ 部署成功标志

当你看到以下提示时，说明部署成功：

```
✨ Success! Uploaded 45 files (2.3 MB)

🌍 Your site is live at:
   https://vben-admin-ailun.pages.dev
```

现在访问该地址，使用凭证登录验证功能！🎉

---

## 🆘 需要帮助？

如果部署过程中遇到问题：

1. **查看 Cloudflare 日志**
   - Dashboard → Pages → 项目 → Deployments

2. **检查 Functions 日志**
   - Dashboard → Pages → 项目 → Functions → Logs

3. **测试本地预览**
   ```bash
   pnpm preview:mock
   ```

4. **参考部署指南**
   - [CLOUDFLARE_DEPLOYMENT.md](CLOUDFLARE_DEPLOYMENT.md)

