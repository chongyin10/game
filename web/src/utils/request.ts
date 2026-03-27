import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { message } from '@zjpcy/simple-design'

// 创建 axios 实例
const request: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // 允许跨域携带 cookie
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // cookie 会自动携带，无需手动设置
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  (error) => {
    // 统一错误处理
    const status = error.response?.status
    const responseData = error.response?.data
    const errorMessage = responseData?.message || error.message || '请求失败'
    
    console.error('API Error:', errorMessage)
    
    // 处理 401 未授权错误（token 过期或未登录）
    if (status === 401) {
      message.error(responseData?.message || '登录已过期，请重新登录')
      
      // 延迟跳转到登录页，让用户看到提示
      setTimeout(() => {
        // 清除可能存在的本地状态
        // TODO: 清除用户信息 store
        
        // 跳转到首页（登录页）
        window.location.href = '/'
      }, 1500)
    }
    
    return Promise.reject(error)
  }
)

// 封装请求方法
export const http = {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return request.get(url, config)
  },

  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return request.post(url, data, config)
  },

  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return request.put(url, data, config)
  },

  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return request.delete(url, config)
  },
}

export default request
