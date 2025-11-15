import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw, NavigationGuardNext } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { usePermissionStore } from '@/store/modules/permission'

// 公开路由（不需要身份验证）
const publicRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: {
      title: '登录'
    }
  }
]

// 需要动态注册的路由（需要身份验证）
const asyncRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: {
      title: '首页',
      requiresAuth: true,
      roles: ['admin', 'user']
    }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: {
      title: '仪表盘',
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('@/views/UsersView/UsersView.vue'),
    meta: {
      title: '用户管理',
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/roles',
    name: 'roles',
    component: () => import('@/views/RolesView/RolesView.vue'),
    meta: {
      title: '角色管理',
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/permissions',
    name: 'permissions',
    component: () => import('@/views/PermissionsView/PermissionsView.vue'),
    meta: {
      title: '权限管理',
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/SettingsView.vue'),
    meta: {
      title: '设置',
      requiresAuth: true,
      roles: ['admin', 'user']
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: {
      title: '个人中心',
      requiresAuth: true,
      roles: ['admin', 'user']
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: publicRoutes
})

// 标记：是否已经添加了动态路由
let isRouteAdded = false

/**
 * 重置路由添加标志（用于登出时重置状态）
 */
export function resetRouteAdded() {
  isRouteAdded = false
}

/**
 * 路由守卫：处理身份验证和权限检查
 */
router.beforeEach(
  async (to, _from, next: NavigationGuardNext) => {
    const userStore = useUserStore()
    const permissionStore = usePermissionStore()

    // 检查是否已登录
    const hasToken = !!userStore.token

    // 如果是登录页面
    if (to.path === '/login') {
      if (hasToken) {
        // 已登录则重定向到首页或目标页面
        const redirect = (to.query.redirect as string) || '/'
        next({ path: redirect })
      } else {
        // 未登录则允许访问登录页
        next()
      }
      return
    }

    // 访问需要身份验证的页面（包括根路径）
    // 注意：对于动态路由，to.meta 可能还没有，所以需要检查路径
    const isProtectedRoute = to.meta?.requiresAuth || 
                            to.path === '/' || 
                            asyncRoutes.some(route => route.path === to.path)
    
    if (isProtectedRoute) {
      if (!hasToken) {
        // 没有 Token，重定向到登录，并保存目标路径
        next({ path: '/login', query: { redirect: to.fullPath } })
        return
      }

      // 检查权限 - 如果还没有添加动态路由
      if (!isRouteAdded) {
        try {
          // 获取用户信息（如果还没有）
          if (!userStore.userInfo) {
            await userStore.getCurrentUser()
          }

          // 生成动态路由（基于用户角色）
          const roles = userStore.userRoles || []
          permissionStore.generateRoutes(roles)

          // 添加异步路由
          asyncRoutes.forEach((route) => {
            router.addRoute(route)
          })

          // 添加 404 路由（必须在最后）
          router.addRoute({
            path: '/:pathMatch(.*)*',
            redirect: '/'
          })

          isRouteAdded = true

          // 重新导航到目标路由，确保动态路由生效
          next({ ...to, replace: true })
          return
        } catch (error) {
          console.error('获取用户信息失败:', error)
          // 如果获取用户信息失败，清除 Token 并重定向到登录页
          userStore.resetStore()
          next({ path: '/login', query: { redirect: to.fullPath } })
          return
        }
      }

      // 检查角色权限
      const requiredRoles = to.meta?.roles as string[] | undefined
      if (requiredRoles && requiredRoles.length > 0) {
        const hasRole = userStore.userRoles.some((role: string) => requiredRoles.includes(role))
        if (!hasRole) {
          // 无权访问，重定向到首页
          next({ path: '/' })
          return
        }
      }

      next()
      return
    }

    // 其他情况（未定义的路由）重定向到登录或首页
    if (!hasToken) {
      next({ path: '/login', query: { redirect: to.fullPath } })
      return
    }

    // 其他情况允许访问
    next()
  }
)

// 在应用初始化时立即添加动态路由（如果用户已登录）
function initializeRoutes() {
  const userStore = useUserStore()
  const permissionStore = usePermissionStore()
  
  // 如果用户已登录且有 Token，尝试初始化路由
  if (userStore.token && !isRouteAdded) {
    // 如果用户信息已存在，直接使用
    if (userStore.userInfo && userStore.userRoles.length > 0) {
      const roles = userStore.userRoles || []
      permissionStore.generateRoutes(roles)
      asyncRoutes.forEach((route) => {
        router.addRoute(route)
      })
      router.addRoute({
        path: '/:pathMatch(.*)*',
        redirect: '/'
      })
      isRouteAdded = true
    }
    // 如果用户信息不存在，会在路由守卫中通过 getCurrentUser 获取
  }
}

// 在路由准备好时初始化
router.isReady().then(() => {
  initializeRoutes()
})

router.afterEach((to) => {
  import('@/store/modules/tabs').then(({ useTabsStore }) => {
    // 在 Pinia 实例化后才能获取 store
    const tabsStore = useTabsStore()
    tabsStore.addTab(to)
  })
})

export default router
