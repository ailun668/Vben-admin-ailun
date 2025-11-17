# 📋 迁移文档：禁用用户登录 Mock 功能

## 变更概览

- **变更日期**：2025-11-17
- **变更类型**：Breaking Change（破坏性变更）
- **影响范围**：开发和生产环境的用户登录流程

## 做了什么？

### ✅ 已完成的变更

1. **移除 Mock 登录接口** (`src/mock/user.ts`)
   - ❌ 删除：`POST /api/user/login` mock 实现
   - ❌ 删除：`GET /api/user/info` mock 实现
   - ❌ 删除：`POST /api/user/logout` mock 实现
   - ✅ 保留：`GET /api/user/list` 用于用户列表展示

2. **更新环境配置**
   - 更新 `.env.development` - 指向本地后端：`http://localhost:8080/api`
   - 更新 `.env.production` - 指向生产后端：`https://vben-admin-ailun.pages.dev/api`

3. **Vite Mock 插件仍然启用**
   - 仅禁用了登录相关的 mock 接口
   - 其他接口（如用户列表）的 mock 仍然可用（便于本地开发）

## 后续步骤

### 📝 必需配置（开发环境）

你的本地后端服务器必须支持以下接口：

```bash
# 1. 登录接口
POST /api/user/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

# 响应格式（必须一致）：
{
  "code": 0,
  "data": {
    "token": "xxxx_token_xxxx",
    "user": {
      "id": "1",
      "username": "admin",
      "realName": "管理员",
      "email": "admin@example.com",
      "avatar": "https://...",
      "roles": ["admin"],
      "permissions": ["system:user:list", ...]
    }
  },
  "message": "登录成功"
}
```

```bash
# 2. 获取当前用户信息接口
GET /api/user/info
Authorization: Bearer {token}

# 响应格式（必须一致）：
{
  "code": 0,
  "data": {
    "id": "1",
    "username": "admin",
    "realName": "管理员",
    "email": "admin@example.com",
    "avatar": "https://...",
    "roles": ["admin"],
    "permissions": ["system:user:list", ...]
  },
  "message": "获取成功"
}
```

```bash
# 3. 登出接口
POST /api/user/logout
Authorization: Bearer {token}

# 响应格式：
{
  "code": 0,
  "data": null,
  "message": "登出成功"
}
```

### 🔧 配置后端地址

编辑 `.env.development`，根据你的实际后端服务器地址修改：

```bash
# 本地开发服务器
VITE_API_BASE_URL=http://localhost:8080/api

# 或远程开发服务器
VITE_API_BASE_URL=https://dev-api.example.com/api
```

> ⚠️ **重要**：修改环境变量后，需要重启开发服务器（`pnpm dev`）才能生效

### ✨ 测试登录流程

1. **启动开发服务器**
   ```bash
   pnpm dev
   ```

2. **打开浏览器** → `http://localhost:5174/login`

3. **输入用户名和密码**
   - 用户名：`admin`
   - 密码：`admin123`

4. **观察浏览器开发工具**（DevTools）
   - Network 标签：应该看到真实的 `POST /api/user/login` 请求
   - 请求目标应该是你配置的后端地址（如 `http://localhost:8080/api/user/login`）

### 🚨 故障排查

#### 问题：登录时提示"用户名或密码错误"

**可能原因**：
1. 后端服务未启动 → 检查后端服务状态
2. 后端地址配置错误 → 检查 `.env.development` 中的 `VITE_API_BASE_URL`
3. 响应格式不对 → 后端需要返回 `{ code: 0, data: {...}, message: '...' }` 格式

**排查步骤**：
```bash
# 1. 检查后端是否运行
curl http://localhost:8080/api/user/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. 检查浏览器 DevTools
# - Network 标签看请求 URL 是否正确
# - Console 标签看是否有错误信息
# - 看响应内容是否符合格式要求
```

#### 问题：登录成功但无法进入应用

**可能原因**：
1. Token 格式不对 → 后端需要返回字符串格式的 token
2. 获取用户信息失败 → 后端 `/api/user/info` 接口有问题
3. 响应中缺少 `roles` 或 `permissions` 字段 → 后端需要返回完整的用户信息

**排查步骤**：
```bash
# 1. 获取 token（从登录响应中复制）
token="xxxx_token_xxxx"

# 2. 测试获取用户信息接口
curl http://localhost:8080/api/user/info \
  -H "Authorization: Bearer $token"

# 3. 检查响应中是否包含 roles 和 permissions 字段
```

## 回滚步骤（如需恢复 Mock）

如果需要临时恢复 mock 登录功能进行测试，请按以下步骤操作：

1. **恢复 mock 接口定义**
   ```bash
   git checkout HEAD -- src/mock/user.ts
   ```

2. **恢复环境变量**
   ```bash
   git checkout HEAD -- .env.development
   ```

3. **重启开发服务器**
   ```bash
   pnpm dev
   ```

## 相关文件

| 文件 | 变更 | 说明 |
|------|------|------|
| `src/mock/user.ts` | 删除登录接口 | 移除了 3 个 mock 接口 |
| `.env.development` | 修改 API 地址 | 指向本地后端 |
| `.env.production` | 补充注释 | 生产环境已配置真实后端 |
| `src/api/user.ts` | 无变更 | 继续调用相同的 API 端点 |
| `src/api/http.ts` | 无变更 | 已支持自定义 API 地址 |

## 常见问题 (FAQ)

**Q: 为什么要禁用 Mock 登录？**
A: Mock 数据只适合开发初期。实际项目需要连接真实后端，确保登录流程与生产环境一致。

**Q: 其他 Mock 接口还能用吗？**
A: 可以。用户列表等接口的 mock 仍然启用，方便本地开发和测试。

**Q: 如果我想要一个快速的本地演示？**
A: 可以临时启用 mock（见上面的"回滚步骤"），但不推荐用于真实开发。

**Q: 后端需要什么框架？**
A: 无限制。只要能实现指定的 API 端点和响应格式即可（Node、Python、Java 等都可以）。

---

**文档维护者**：Claude Code
**最后更新**：2025-11-17
