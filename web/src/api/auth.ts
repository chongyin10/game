import { http } from '@/utils/request'
import type {
  ApiResponse,
  RegisterParams,
  LoginParams,
  LoginData,
  RegisterData,
} from '@/types'

const BASE_URL = '/auth'

// 用户注册
export const register = (data: RegisterParams) => {
  return http.post<ApiResponse<RegisterData>>(`${BASE_URL}/register`, data)
}

// 用户登录
export const login = (data: LoginParams) => {
  return http.post<ApiResponse<LoginData>>(`${BASE_URL}/login`, data)
}
