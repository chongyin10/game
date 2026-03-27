"""
统一响应封装工具模块

提供标准化的 API 响应格式：
{
    "success": True/False,
    "message": "提示信息",
    "data": 数组、对象、布尔值、字符串、数字等
}

使用方法:
    from core.response import success_response, error_response, ResponseCode
    
    # 成功响应 - 返回对象
    return success_response(data={"id": 1, "name": "张三"}, message="获取成功")
    
    # 成功响应 - 返回数组
    return success_response(data=[{"id": 1}, {"id": 2}], message="列表获取成功")
    
    # 成功响应 - 返回布尔值
    return success_response(data=True, message="操作成功")
    
    # 错误响应
    return error_response(message="用户不存在", code=ResponseCode.NOT_FOUND)
"""

from typing import Any, Optional
from enum import IntEnum


class ResponseCode(IntEnum):
    """HTTP 状态码常量"""
    OK = 200                    # 成功
    CREATED = 201              # 创建成功
    BAD_REQUEST = 400          # 请求参数错误
    UNAUTHORIZED = 401         # 未授权
    FORBIDDEN = 403            # 禁止访问
    NOT_FOUND = 404            # 资源不存在
    CONFLICT = 409             # 资源冲突
    INTERNAL_ERROR = 500       # 服务器内部错误


def success_response(
    data: Any = None,
    message: str = "操作成功",
    code: int = ResponseCode.OK
) -> tuple[dict[str, Any], int]:
    """
    生成成功响应
    
    Args:
        data: 响应数据（可以是对象、数组、布尔值、字符串、数字等）
        message: 成功提示信息
        code: HTTP 状态码，默认 200
        
    Returns:
        tuple: (响应字典, HTTP 状态码)
        
    Examples:
        >>> success_response(data={"id": 1}, message="获取成功")
        ({"success": True, "message": "获取成功", "data": {"id": 1}}, 200)
        
        >>> success_response(data=[{"id": 1}, {"id": 2}])
        ({"success": True, "message": "操作成功", "data": [{"id": 1}, {"id": 2}]}, 200)
        
        >>> success_response(data=True, message="删除成功")
        ({"success": True, "message": "删除成功", "data": True}, 200)
    """
    return {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }, code


def error_response(
    message: str = "操作失败",
    code: int = ResponseCode.BAD_REQUEST,
    data: Any = None
) -> tuple[dict[str, Any], int]:
    """
    生成错误响应
    
    Args:
        message: 错误提示信息
        code: HTTP 状态码，默认 400
        data: 可选的错误详情数据
        
    Returns:
        tuple: (响应字典, HTTP 状态码)
        
    Examples:
        >>> error_response(message="用户不存在", code=ResponseCode.NOT_FOUND)
        ({"success": False, "message": "用户不存在", "data": {}}, 404)
        
        >>> error_response(message="参数错误", data={"field": "username"})
        ({"success": False, "message": "参数错误", "data": {"field": "username"}}, 400)
    """
    response = {
        "success": False,
        "message": message,
        "data": data if data is not None else {}
    }
    return response, code


def created_response(
    data: Any = None,
    message: str = "创建成功"
) -> tuple[dict[str, Any], int]:
    """
    生成创建成功响应（HTTP 201）
    
    Args:
        data: 创建的资源的响应数据
        message: 成功提示信息
        
    Returns:
        tuple: (响应字典, HTTP 状态码 201)
    """
    return success_response(data=data, message=message, code=ResponseCode.CREATED)


def list_response(
    data: list[Any],
    total: Optional[int] = None,
    message: str = "获取成功"
) -> tuple[dict[str, Any], int]:
    """
    生成列表数据响应
    
    Args:
        data: 列表数据数组
        total: 总记录数（用于分页）
        message: 成功提示信息
        
    Returns:
        tuple: (响应字典, HTTP 状态码)
        
    Examples:
        >>> list_response(data=[{"id": 1}], total=100)
        ({"success": True, "message": "获取成功", "data": [{"id": 1}], "total": 100}, 200)
    """
    response: dict[str, Any] = {
        "success": True,
        "message": message,
        "data": data if data is not None else []
    }
    if total is not None:
        response["total"] = total
    return response, ResponseCode.OK


# 导出所有公共接口
__all__ = [
    "success_response",
    "error_response", 
    "created_response",
    "list_response",
    "ResponseCode"
]
