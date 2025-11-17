/**
 * Cloudflare Workers - 获取用户信息接口
 * 部署路径: /api/user/info
 */

const USERS = {
  admin: {
    id: '1',
    username: 'admin',
    realName: '管理员',
    email: 'admin@example.com',
    avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
    roles: ['admin'],
    permissions: ['system:user:list', 'system:user:add', 'system:user:edit', 'system:user:delete']
  },
  user: {
    id: '2',
    username: 'user',
    realName: '普通用户',
    email: 'user@example.com',
    avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
    roles: ['user'],
    permissions: ['system:user:list', 'system:user:edit']
  }
};

const TOKEN_MAP = {
  'admin_token_12345': 'admin',
  'user_token_67890': 'user'
};

export async function onRequest(context) {
  const request = context.request;

  // 仅处理 GET 请求
  if (request.method !== 'GET') {
    return new Response('Method not allowed', { status: 405 });
  }

  try {
    // 获取 Authorization 请求头
    const authHeader = request.headers.get('authorization') || '';
    const token = authHeader.replace('Bearer ', '').trim();

    // 验证 token
    const username = TOKEN_MAP[token];
    if (username && USERS[username]) {
      return new Response(
        JSON.stringify({
          code: 0,
          data: USERS[username],
          message: '获取成功'
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    } else {
      return new Response(
        JSON.stringify({
          code: 401,
          data: null,
          message: 'Token无效或已过期'
        }),
        {
          status: 401,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
  } catch (error) {
    return new Response(
      JSON.stringify({
        code: 500,
        data: null,
        message: '服务器错误'
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}
