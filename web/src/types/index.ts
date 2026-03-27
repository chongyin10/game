// API 响应通用类型
export interface ApiResponse<T = any> {
  success: boolean
  message?: string
  data?: T
  total?: number
}

// 用户信息类型
export interface User {
  id: string
  username: string
  email?: string
  phone?: string
  password?: string
  created_at?: string
  updated_at?: string
}

// 用户查询参数
export interface UserQueryParams {
  user_id?: string
  username?: string
  email?: string
  phone?: string
}

// 用户列表查询参数
export interface UserListParams {
  limit?: number
  offset?: number
}

// 添加用户参数
export interface AddUserParams {
  username: string
  email?: string
  phone?: string
  password?: string
}

// 更新用户参数
export interface UpdateUserParams {
  user_id: string
  username?: string
  email?: string
  phone?: string
  password?: string
}

// 注册参数
export interface RegisterParams {
  username: string
  email?: string
  phone?: string
  password: string
  confirm_password: string
}

// 登录参数
export interface LoginParams {
  username?: string
  email?: string
  phone?: string
  password: string
}

// 登录响应数据
export interface LoginData {
  user: User
}

// 注册响应数据
export interface RegisterData {
  user_id: string
}
