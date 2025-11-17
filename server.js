/**
 * 生产预览服务器 - 支持 Mock API
 *
 * 用法：
 *   pnpm build
 *   pnpm preview:mock
 *
 * 访问：http://localhost:4176
 *
 * 说明：
 * - 提供静态文件服务（dist 目录）
 * - 集成 Mock API（同开发环境）
 * - 支持 SPA 路由
 */

import express from 'express';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

// 获取 __dirname（ES Module 中需要手动定义）
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 4176;
const DIST_DIR = path.resolve(__dirname, 'dist');

// ============ 中间件 ============
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 日志中间件
app.use((req, res, next) => {
  if (!req.path.startsWith('/api')) {
    console.log(`${new Date().toLocaleTimeString()} ${req.method} ${req.path}`);
  }
  next();
});

// ============ Mock API 数据 ============
const users = {
  admin: {
    id: '1',
    username: 'admin',
    realName: '管理员',
    email: 'admin@example.com',
    avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
    roles: ['admin'],
    permissions: [
      'system:user:list',
      'system:user:add',
      'system:user:edit',
      'system:user:delete',
      'system:role:list',
      'system:role:add',
      'system:role:edit',
      'system:role:delete',
      'system:permission:list',
      'system:permission:add',
      'system:permission:edit',
      'system:permission:delete'
    ]
  },
  user: {
    id: '2',
    username: 'user',
    realName: '普通用户',
    email: 'user@example.com',
    avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
    roles: ['user'],
    permissions: [
      'system:user:list',
      'system:user:edit'
    ]
  }
};

const tokenMap = {
  'admin_token_12345': 'admin',
  'user_token_67890': 'user'
};

// ============ Mock API 路由 ============

/**
 * 登录接口
 */
app.post('/api/user/login', (req, res) => {
  const { username, password } = req.body;

  if (username === 'admin' && password === 'admin123') {
    return res.json({
      code: 0,
      data: {
        token: 'admin_token_12345',
        user: users.admin
      },
      message: '登录成功'
    });
  } else if (username === 'user' && password === 'user123') {
    return res.json({
      code: 0,
      data: {
        token: 'user_token_67890',
        user: users.user
      },
      message: '登录成功'
    });
  } else {
    return res.status(401).json({
      code: 401,
      data: null,
      message: '用户名或密码错误'
    });
  }
});

/**
 * 获取当前用户信息接口
 */
app.get('/api/user/info', (req, res) => {
  const authHeader = req.get('authorization') || '';
  const token = authHeader.replace('Bearer ', '');

  const username = tokenMap[token];
  if (username && users[username]) {
    return res.json({
      code: 0,
      data: users[username],
      message: '获取成功'
    });
  } else {
    return res.status(401).json({
      code: 401,
      data: null,
      message: 'Token无效或已过期'
    });
  }
});

/**
 * 登出接口
 */
app.post('/api/user/logout', (req, res) => {
  res.json({
    code: 0,
    data: null,
    message: '登出成功'
  });
});

/**
 * 获取用户列表接口
 */
app.get('/api/user/list', (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const pageSize = parseInt(req.query.pageSize) || 10;
  const searchText = (req.query.search || '').toLowerCase();

  // 生成模拟数据
  const mockUsers = Array.from({ length: 100 }, (_, i) => ({
    id: `${i + 1}`,
    username: `user${i + 1}`,
    realName: `用户${i + 1}`,
    email: `user${i + 1}@example.com`,
    status: i % 2 === 0 ? 'active' : 'inactive',
    createTime: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000)
      .toISOString()
      .split('T')[0]
  }));

  let filtered = mockUsers;
  if (searchText) {
    filtered = filtered.filter(u =>
      u.username.toLowerCase().includes(searchText) ||
      u.realName.toLowerCase().includes(searchText) ||
      u.email.toLowerCase().includes(searchText)
    );
  }

  const total = filtered.length;
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  const list = filtered.slice(start, end);

  res.json({
    code: 0,
    data: {
      list,
      page,
      pageSize,
      total,
      pageCount: Math.ceil(total / pageSize)
    },
    message: '获取成功'
  });
});

// ============ 静态文件和 SPA 路由 ============

// 提供静态文件
app.use(express.static(DIST_DIR, {
  maxAge: '1h',
  etag: false
}));

// SPA 路由处理 - 所有未匹配的路由返回 index.html
app.get('*', (req, res) => {
  const indexPath = path.join(DIST_DIR, 'index.html');

  if (!fs.existsSync(indexPath)) {
    return res.status(404).send(
      '❌ dist/index.html 不存在，请先执行 pnpm build'
    );
  }

  res.sendFile(indexPath);
});

// ============ 启动服务器 ============
app.listen(PORT, () => {
  console.log('\n' + '='.repeat(70));
  console.log('🚀 生产预览服务器已启动（支持 Mock API）');
  console.log('='.repeat(70));
  console.log(`\n📍 访问地址:     http://localhost:${PORT}`);
  console.log(`📁 静态资源:     ${DIST_DIR}`);
  console.log(`🔌 Mock API 前缀: /api`);
  console.log('\n🔑 测试凭证:');
  console.log('   管理员 - 用户名: admin   密码: admin123');
  console.log('   普通用户 - 用户名: user   密码: user123');
  console.log('\n💡 提示:');
  console.log('   - 这个服务器集成了与开发环境一致的 Mock API');
  console.log('   - 可以测试打包后应用的完整功能');
  console.log('   - 生产环境需要配置真实的后端 API');
  console.log('\n' + '='.repeat(70) + '\n');
});

// 错误处理
process.on('uncaughtException', (error) => {
  console.error('❌ 服务器错误:', error);
  process.exit(1);
});
