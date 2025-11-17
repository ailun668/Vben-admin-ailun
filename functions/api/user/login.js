/**
 * Cloudflare Workers - 用户登录接口
 * 部署路径: /api/user/login
 */

// Mock 用户数据
const USERS = {
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

export async function onRequest(context) {
  const request = context.request;

  // 仅处理 POST 请求
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }

  try {
    const body = await request.json();
    const { username, password } = body;

    // 验证凭证
    if (username === 'admin' && password === 'admin123') {
      return new Response(
        JSON.stringify({
          code: 0,
          data: {
            token: 'admin_token_12345',
            user: USERS.admin
          },
          message: '登录成功'
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    } else if (username === 'user' && password === 'user123') {
      return new Response(
        JSON.stringify({
          code: 0,
          data: {
            token: 'user_token_67890',
            user: USERS.user
          },
          message: '登录成功'
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
          message: '用户名或密码错误'
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
