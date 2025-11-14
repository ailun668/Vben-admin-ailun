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
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
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
      requiresAuth: true
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
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: publicRoutes
})

// 标记：是否已经添加了动态路由
let isRouteAdded = false

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
        // 已登录则重定向到首页
        next({ path: '/' })
      } else {
        // 未登录则允许访问登录页
        next()
      }
      return
    }

    // 访问需要身份验证的页面
    if (to.meta?.requiresAuth) {
      if (!hasToken) {
        // 没有 Token，重定向到登录
        next({ path: '/login', query: { redirect: to.fullPath } })
        return
      }

      // 检查权限
      if (!isRouteAdded) {
        // 生成动态路由（基于用户角色）
        const roles = userStore.userRoles
        permissionStore.generateRoutes(roles)

        // 添加异步路由
        asyncRoutes.forEach((route) => {
          router.addRoute(route)
        })

        isRouteAdded = true

        // 重新导航到目标路由，确保动态路由生效
        next({ ...to, replace: true })
        return
      }

      // 检查角色权限
      const requiredRoles = to.meta.roles as string[] | undefined
      if (requiredRoles && requiredRoles.length > 0) {
        const hasRole = userStore.userRoles.some((role: string) => requiredRoles.includes(role))
        if (!hasRole) {
          next({ path: '/login' })
          return
        }
      }

      next()
      return
    }

    // 其他情况允许访问
    next()
  }
)

export default router
