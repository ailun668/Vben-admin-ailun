/**
 * Cloudflare Workers - 获取用户列表接口
 * 部署路径: /api/user/list
 */

function generateMockUsers(count = 100) {
  const users = [];
  for (let i = 1; i <= count; i++) {
    users.push({
      id: `${i}`,
      username: `user${i}`,
      realName: `用户${i}`,
      email: `user${i}@example.com`,
      status: i % 2 === 0 ? 'active' : 'inactive',
      createTime: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000)
        .toISOString()
        .split('T')[0]
    });
  }
  return users;
}

export async function onRequest(context) {
  const request = context.request;

  // 仅处理 GET 请求
  if (request.method !== 'GET') {
    return new Response('Method not allowed', { status: 405 });
  }

  try {
    const url = new URL(request.url);
    const page = parseInt(url.searchParams.get('page')) || 1;
    const pageSize = parseInt(url.searchParams.get('pageSize')) || 10;
    const searchText = (url.searchParams.get('search') || '').toLowerCase();

    // 获取模拟数据
    const mockUsers = generateMockUsers(100);

    // 搜索过滤
    let filtered = mockUsers;
    if (searchText) {
      filtered = filtered.filter(u =>
        u.username.toLowerCase().includes(searchText) ||
        u.realName.toLowerCase().includes(searchText) ||
        u.email.toLowerCase().includes(searchText)
      );
    }

    // 分页
    const total = filtered.length;
    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    const list = filtered.slice(start, end);

    return new Response(
      JSON.stringify({
        code: 0,
        data: {
          list,
          page,
          pageSize,
          total,
          pageCount: Math.ceil(total / pageSize)
        },
        message: '获取成功'
      }),
      {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
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
