/**
 * 预览服务器 - 支持 Mock API
 *
 * 用法：
 *   node preview-server.js
 *
 * 访问：http://localhost:4176
 *
 * 说明：
 * - 加载 vite-plugin-mock 的中间件
 * - 代理生产构建的静态文件
 * - 支持 Mock API 就像开发环境一样
 */

const express = require('express');
const path = require('path');
const fs = require('fs');

// 导入 vite-plugin-mock 的中间件
const { createMockMiddleware } = require('vite-plugin-mock/dist/middleware');

const app = express();
const PORT = process.env.PORT || 4176;
const DIST_DIR = path.resolve(__dirname, 'dist');

// 中间件：解析 JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 日志中间件
app.use((req, res, next) => {
  console.log(`${new Date().toLocaleTimeString()} ${req.method} ${req.path}`);
  next();
});

// Mock API 中间件（需要 vite-plugin-mock）
try {
  const mockMiddleware = createMockMiddleware({
    mockPath: path.resolve(__dirname, 'src/mock'),
    prefix: '/api'
  });
  app.use('/api', mockMiddleware);
  console.log('✅ Mock API 中间件已加载');
} catch (error) {
  console.warn('⚠️ Mock API 中间件加载失败，请确保已安装依赖:', error.message);
  // 继续运行，不中断启动
}

// 静态文件服务（生产构建的输出）
app.use(express.static(DIST_DIR, {
  maxAge: '1h',
  etag: false
}));

// 单页应用路由处理（处理 Vue Router）
app.get('*', (req, res) => {
  // 检查是否是 API 请求（已被 mock 中间件处理）
  if (req.path.startsWith('/api')) {
    return res.status(404).json({ code: 404, message: '接口不存在' });
  }

  // 返回 index.html
  const indexPath = path.join(DIST_DIR, 'index.html');
  if (fs.existsSync(indexPath)) {
    res.sendFile(indexPath);
  } else {
    res.status(404).send('dist/index.html 不存在，请先执行 pnpm build');
  }
});

// 启动服务器
app.listen(PORT, () => {
  console.log('\n' + '='.repeat(60));
  console.log('📦 预览服务器已启动');
  console.log('='.repeat(60));
  console.log(`\n🌐 访问地址: http://localhost:${PORT}`);
  console.log(`📁 静态文件目录: ${DIST_DIR}`);
  console.log(`📝 Mock API 前缀: /api`);
  console.log('\n测试登录凭证:');
  console.log('  用户名: admin');
  console.log('  密码: admin123');
  console.log('\n' + '='.repeat(60) + '\n');
});

// 错误处理
process.on('uncaughtException', (error) => {
  console.error('❌ 服务器错误:', error);
  process.exit(1);
});
