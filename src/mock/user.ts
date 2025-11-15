import type { MockMethod } from 'vite-plugin-mock'

// 模拟数据
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
}

// 生成模拟用户列表数据（用于 /api/user/list 接口）
function generateMockUserList(count: number = 100) {
  const statuses = ['active', 'inactive'] as const
  const rolesList = [['admin'], ['user'], ['user', 'editor'], ['viewer']]
  const users = []

  for (let i = 1; i <= count; i++) {
    users.push({
      id: `${i}`,
      username: `user${i}`,
      realName: `用户${i}`,
      email: `user${i}@example.com`,
      avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
      roles: rolesList[i % rolesList.length],
      status: statuses[i % 2],
      createTime: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      permissions: i % 2 === 0 ? ['user:view', 'user:edit'] : ['user:view']
    })
  }

  return users
}

const userList = generateMockUserList(100)

// 令牌存储（生产环境应该由后端生成）
const tokenMap = {
  'admin_token_12345': 'admin',
  'user_token_67890': 'user'
}

export default [
  // 登录接口
  {
    url: '/api/user/login',
    method: 'post',
    response: ({ body }: any) => {
      const { username, password } = body

      // 模拟验证
      if (username === 'admin' && password === 'admin123') {
        return {
          code: 0,
          data: {
            token: 'admin_token_12345',
            user: users.admin
          },
          message: '登录成功'
        }
      } else if (username === 'user' && password === 'user123') {
        return {
          code: 0,
          data: {
            token: 'user_token_67890',
            user: users.user
          },
          message: '登录成功'
        }
      } else {
        return {
          code: 401,
          data: null,
          message: '用户名或密码错误'
        }
      }
    }
  },

  // 获取当前用户信息接口
  {
    url: '/api/user/info',
    method: 'get',
    response: ({ headers }: any) => {
      const authHeader = headers.authorization || ''
      const token = authHeader.replace('Bearer ', '')

      const username = tokenMap[token as keyof typeof tokenMap]
      if (username && users[username as keyof typeof users]) {
        return {
          code: 0,
          data: users[username as keyof typeof users],
          message: '获取成功'
        }
      } else {
        return {
          code: 401,
          data: null,
          message: 'Token无效或已过期'
        }
      }
    }
  },

  // 登出接口
  {
    url: '/api/user/logout',
    method: 'post',
    response: () => {
      return {
        code: 0,
        data: null,
        message: '登出成功'
      }
    }
  },

  // 获取用户列表接口（支持分页和搜索）
  {
    url: '/api/user/list',
    method: 'get',
    response: ({ url }: any) => {
      // 解析查询参数
      const urlObj = new URL(`http://localhost${url}`)
      const page = parseInt(urlObj.searchParams.get('page') || '1')
      const pageSize = parseInt(urlObj.searchParams.get('pageSize') || '10')
      const searchText = (urlObj.searchParams.get('search') || '').toLowerCase()
      const status = urlObj.searchParams.get('status') || ''

      // 过滤数据
      let filtered = userList
      if (searchText) {
        filtered = filtered.filter(
          (u) => u.username.toLowerCase().includes(searchText) ||
                 u.realName.toLowerCase().includes(searchText) ||
                 u.email.toLowerCase().includes(searchText)
        )
      }
      if (status) {
        filtered = filtered.filter((u) => u.status === status)
      }

      // 分页
      const total = filtered.length
      const start = (page - 1) * pageSize
      const end = start + pageSize
      const list = filtered.slice(start, end)

      return {
        code: 0,
        data: {
          list,
          page,
          pageSize,
          total,
          pageCount: Math.ceil(total / pageSize)
        },
        message: '获取成功'
      }
    }
  },

  // 获取用户列表（原始接口，保留兼容性）
  {
    url: '/api/user',
    method: 'get',
    response: () => {
      return {
        code: 0,
        data: {
          name: 'Gemini',
          age: 1,
          avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4'
        },
        message: '获取成功'
      }
    }
  }
] as MockMethod[]
