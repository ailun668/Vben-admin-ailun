import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'
import { useUserStore } from '@/store/modules/user'
import type { ApiResponse } from './types'

class HttpClient {
  private instance: AxiosInstance

  constructor() {
    this.instance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        const userStore = useUserStore()
        const token = userStore.token

        // 如果有 token，添加到请求头
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }

        return config
      },
      (error) => {
        console.error('请求配置错误:', error)
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response) => {
        const data = response.data as ApiResponse<any>

        // 检查业务状态码
        if (data.code === 0) {
          return response.data
        } else if (data.code === 401) {
          // Token 过期或无效，清除用户信息并跳转到登录
          const userStore = useUserStore()
          userStore.logout()
          window.location.href = '/login'
          return Promise.reject(new Error(data.message || 'Token已过期'))
        } else {
          // 其他业务错误
          return Promise.reject(new Error(data.message || '请求失败'))
        }
      },
      (error) => {
        // 处理网络错误
        if (error.response) {
          const status = error.response.status
          let message = '请求失败'

          switch (status) {
            case 400:
              message = '请求参数错误'
              break
            case 403:
              message = '无权限访问'
              break
            case 404:
              message = '资源不存在'
              break
            case 500:
              message = '服务器错误'
              break
            default:
              message = `网络错误: ${status}`
          }

          console.error(message, error.response)
        } else if (error.request) {
          console.error('无响应:', error.request)
        } else {
          console.error('请求错误:', error.message)
        }

        return Promise.reject(error)
      }
    )
  }

  request<T = any>(config: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.instance.request(config)
  }

  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'GET', url })
  }

  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'POST', url, data })
  }

  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'PUT', url, data })
  }

  patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'PATCH', url, data })
  }

  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'DELETE', url })
  }
}

export const http = new HttpClient()
