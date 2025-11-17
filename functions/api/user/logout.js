/**
 * Cloudflare Workers - 用户登出接口
 * 部署路径: /api/user/logout
 */

export async function onRequest(context) {
  const request = context.request;

  // 仅处理 POST 请求
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }

  return new Response(
    JSON.stringify({
      code: 0,
      data: null,
      message: '登出成功'
    }),
    {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    }
  );
}
