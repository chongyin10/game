import { http } from '@/utils/request'
import type {
  ApiResponse,
  User,
  UserQueryParams,
  UserListParams,
  AddUserParams,
  UpdateUserParams,
} from '@/types'

const BASE_URL = '/userinfo'

// 获取用户列表
export const getUserList = (params?: UserListParams) => {
  return http.get<ApiResponse<User[]>>(`${BASE_URL}/list`, { params })
}

// 获取单个用户
export const getUser = (params: UserQueryParams) => {
  return http.get<ApiResponse<User>>(`${BASE_URL}/get`, { params })
}

// 添加用户
export const addUser = (data: AddUserParams) => {
  return http.post<ApiResponse>(`${BASE_URL}/add`, data)
}

// 更新用户
export const updateUser = (data: UpdateUserParams) => {
  return http.put<ApiResponse>(`${BASE_URL}/update`, data)
}

// 删除用户
export const deleteUser = (userId: number) => {
  return http.delete<ApiResponse>(`${BASE_URL}/delete`, { params: { user_id: userId } })
}
