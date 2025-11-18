# Project Context

## Purpose
这是一个基于 Vue 3 + TypeScript + Vite 构建的企业级管理后台系统。项目实现了完整的用户认证、权限管理、路由控制和数据可视化功能。主要目标是提供一个现代化、高性能、易于扩展的前端管理系统框架。

## Tech Stack
- **前端框架**: Vue 3.5.24 (Composition API + `<script setup>`)
- **开发语言**: TypeScript 5.9.3
- **构建工具**: Vite 7.2.2
- **UI 组件库**: Ant Design Vue 4.2.6
- **图标库**: @ant-design/icons-vue 7.0.1
- **状态管理**: Pinia 3.0.4 + pinia-plugin-persistedstate 4.7.1
- **路由管理**: Vue Router 4.6.3
- **HTTP 客户端**: Axios 1.13.2
- **数据可视化**: ECharts 5.4.3
- **表格组件**: vxe-table 4.4.5
- **Mock 数据**: MockJS 1.1.0 + vite-plugin-mock 3.0.2
- **工具库**: lodash-es 4.17.21, dayjs 1.11.19, crypto-js 4.2.0
- **Excel 处理**: exceljs 4.4.0, xlsx 0.18.5

## Project Conventions

### Code Style
- **全量 JSDoc 注释**: 所有函数、类、接口必须有 JSDoc3 风格注释,注释率 100%
- **中文注释**: 代码注释使用中文,便于团队理解
- **命名规范**:
  - 组件文件: PascalCase (如 `UserView.vue`)
  - 普通文件: kebab-case (如 `user-api.ts`)
  - 变量/函数: camelCase (如 `userInfo`, `getUserData`)
  - 常量: UPPER_SNAKE_CASE (如 `API_BASE_URL`)
- **文件组织**: 按功能模块划分目录 (api/, components/, views/, store/)
- **路径别名**: 使用 `@/` 指向 `src/` 目录

### Architecture Patterns
- **组合式 API**: 统一使用 Vue 3 Composition API
- **状态管理**: Pinia stores 按模块划分 (user, app, permission)
- **API 层**: 统一封装 axios,集中管理 API 接口
- **路由守卫**: 基于角色的权限控制 (RBAC)
- **Mock 数据**: 开发环境使用 vite-plugin-mock,生产环境禁用
- **响应式设计**: 支持桌面端和移动端自适应
- **SOLID 原则**: 高内聚低耦合,单一职责

### Testing Strategy
- **开发测试**: 使用 Mock 数据进行本地开发测试
- **权限测试**: 测试不同角色的菜单和路由访问权限
- **浏览器测试**: 支持主流浏览器 (Chrome, Firefox, Safari, Edge)
- **手动测试**: 参考 QUICK-START.md 进行功能验证

### Git Workflow
- **分支策略**: 功能开发使用 feature 分支
- **提交规范**: 使用语义化提交信息
- **代码审查**: 重要功能需要 Code Review
- **文档同步**: 代码变更需同步更新相关文档

## Domain Context
- **用户角色**: 支持管理员 (admin) 和普通用户 (user) 两种角色
- **权限系统**: 基于角色的菜单显示和路由访问控制
- **登录凭证**: 使用 JWT Token 进行身份认证
- **数据持久化**: 使用 pinia-plugin-persistedstate 持久化用户状态
- **页面模块**:
  - 首页: 欢迎页面
  - 仪表盘: 数据统计和最近访问记录
  - 用户管理: 用户列表和操作
  - 角色管理: 角色配置
  - 权限管理: 权限分配
  - 设置: 系统设置

## Important Constraints
- **浏览器兼容**: 需支持现代浏览器 (ES6+)
- **开发环境**: Node.js 18+ 或 20+
- **包管理器**: 支持 npm 或 pnpm
- **TypeScript 严格模式**: 使用 `skipLibCheck: true` 跳过库检查
- **Mock 数据限制**: 仅在开发环境启用,生产环境必须禁用
- **路由模式**: 使用 HTML5 History 模式

## External Dependencies
- **开发服务器**: Vite Dev Server (http://localhost:5173)
- **Mock 服务**: vite-plugin-mock 提供开发环境 API Mock
- **CDN 资源**: Ant Design Vue 图标和样式
- **部署平台**: 支持 Cloudflare Pages 部署 (参考 CLOUDFLARE_DEPLOYMENT.md)
- **预览服务器**: Express 服务器用于生产预览 (server.js)
