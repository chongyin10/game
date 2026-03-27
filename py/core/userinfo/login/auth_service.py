"""
用户登录注册模块 - 提供用户注册和登录功能

使用方法:
    from core.userinfo.login.auth_service import registerUser, loginUser
    
    # 用户注册
    registerUser(
        username="张三",
        email="zhangsan@example.com",
        phone="13800138000",
        password="123456"
    )
    
    # 用户登录
    loginUser(username="张三", password="123456")
"""

import re
import hashlib
import uuid
from typing import Optional, Any
from db_config import Database
from core.userinfo.user_service import addUser, getUser


def _generate_userid() -> str:
    """生成UUID用户ID"""
    return str(uuid.uuid4())


def _hash_password(password: str) -> str:
    """
    对密码进行 SHA256 哈希加密
    
    Args:
        password: 原始密码
        
    Returns:
        str: 加密后的密码
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def _validate_username(username: str) -> tuple[bool, str]:
    """
    验证用户名
    
    Args:
        username: 用户名
        
    Returns:
        tuple[bool, str]: (是否有效, 错误信息)
    """
    if not username or len(username) < 3:
        return False, "用户名长度至少为3个字符"
    if len(username) > 50:
        return False, "用户名长度不能超过50个字符"
    if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', username):
        return False, "用户名只能包含字母、数字、下划线或中文"
    return True, ""


def _validate_email(email: str) -> tuple[bool, str]:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        tuple[bool, str]: (是否有效, 错误信息)
    """
    if not email:
        return True, ""  # 邮箱为空时允许通过
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "邮箱格式不正确"
    return True, ""


def _validate_phone(phone: str) -> tuple[bool, str]:
    """
    验证手机号格式
    
    Args:
        phone: 手机号码
        
    Returns:
        tuple[bool, str]: (是否有效, 错误信息)
    """
    if not phone:
        return True, ""  # 手机号为空时允许通过
    # 中国大陆手机号格式
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone):
        return False, "手机号格式不正确"
    return True, ""


def _validate_password(password: str, confirm_password: str) -> tuple[bool, str]:
    """
    验证密码
    
    Args:
        password: 密码
        confirm_password: 确认密码
        
    Returns:
        tuple[bool, str]: (是否有效, 错误信息)
    """
    if not password:
        return False, "密码不能为空"
    if len(password) < 6:
        return False, "密码长度至少为6个字符"
    if len(password) > 128:
        return False, "密码长度不能超过128个字符"
    if password != confirm_password:
        return False, "两次输入的密码不一致"
    return True, ""


def _check_user_exists(username: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None) -> tuple[bool, str]:
    """
    检查用户是否已存在
    
    Args:
        username: 用户名
        email: 邮箱
        phone: 手机号
        
    Returns:
        tuple[bool, str]: (是否存在, 错误信息)
    """
    if username:
        existing = getUser(username=username)
        if existing:
            return True, "用户名已被注册"
    
    if email:
        existing = getUser(email=email)
        if existing:
            return True, "邮箱已被注册"
    
    if phone:
        existing = getUser(phone=phone)
        if existing:
            return True, "手机号已被注册"
    
    return False, ""


def registerUser(
    username: str,
    email: str,
    phone: str,
    password: str,
    confirm_password: str
) -> dict[str, Any]:
    """
    用户注册
    
    注册新用户到 userinfo 表，包含完整的参数验证。
    
    Args:
        username: 用户名（必填）
        email: 邮箱地址（可选）
        phone: 手机号码（可选）
        password: 密码（必填）
        confirm_password: 确认密码（必填）
        
    Returns:
        dict: 注册结果
        {
            "success": True/False,
            "message": "成功或错误信息",
            "data": {"user_id": 用户ID} (注册成功时) 或 {}
        }
        
    Example:
        >>> registerUser(
        ...     username="张三",
        ...     email="zhangsan@example.com",
        ...     phone="13800138000",
        ...     password="123456",
        ...     confirm_password="123456"
        ... )
        {"success": True, "message": "注册成功", "data": {"user_id": "xxx"}}
    """
    # 1. 验证用户名
    valid, error = _validate_username(username)
    if not valid:
        return {"success": False, "message": error, "data": {}}
    
    # 2. 验证邮箱（可选）
    valid, error = _validate_email(email)
    if not valid:
        return {"success": False, "message": error, "data": {}}
    
    # 3. 验证手机号（可选）
    valid, error = _validate_phone(phone)
    if not valid:
        return {"success": False, "message": error, "data": {}}
    
    # 4. 验证密码
    valid, error = _validate_password(password, confirm_password)
    if not valid:
        return {"success": False, "message": error, "data": {}}
    
    # 5. 检查用户是否已存在
    exists, error = _check_user_exists(username=username, email=email if email else None, phone=phone if phone else None)
    if exists:
        return {"success": False, "message": error, "data": {}}
    
    # 6. 加密密码
    hashed_password = _hash_password(password)
    
    # 7. 生成用户ID
    user_id = _generate_userid()
    
    # 8. 创建用户
    try:
        with Database() as db:
            # 先执行插入
            insert_query = """
                INSERT INTO userinfo (userid, username, email, phone, password)
                VALUES (%s, %s, %s, %s, %s)
            """
            success = db.execute_update(insert_query, (user_id, username, email if email else None, phone if phone else None, hashed_password))
            
            if success:
                return {
                    "success": True,
                    "message": "注册成功",
                    "data": {"user_id": user_id}
                }
            else:
                return {
                    "success": False,
                    "message": "注册失败，请稍后重试",
                    "data": {}
                }
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"[ERROR] 注册异常: {error_detail}")
        return {
            "success": False,
            "message": f"注册失败: {str(e)}",
            "data": {}
        }


def loginUser(
    username: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    password: str = ""
) -> dict[str, Any]:
    """
    用户登录
    
    支持通过用户名、邮箱或手机号登录。
    
    Args:
        username: 用户名（可选，与 email/phone 至少提供一个）
        email: 邮箱（可选）
        phone: 手机号（可选）
        password: 密码（必填）
        
    Returns:
        dict: 登录结果
        {
            "success": True/False,
            "message": "成功或错误信息",
            "data": 用户信息 (登录成功时) 或 {}
        }
        
    Example:
        >>> loginUser(username="张三", password="123456")
        {"success": True, "message": "登录成功", "data": {...}}
        
        >>> loginUser(email="zhangsan@example.com", password="123456")
        {"success": True, "message": "登录成功", "data": {...}}
    """
    if not password:
        return {"success": False, "message": "密码不能为空", "data": {}}
    
    # 至少需要一个登录凭证
    if not any([username, email, phone]):
        return {"success": False, "message": "请提供用户名、邮箱或手机号", "data": {}}
    
    # 查询用户
    user = getUser(username=username, email=email, phone=phone)
    
    if not user:
        return {"success": False, "message": "用户不存在", "data": {}}
    
    # 验证密码
    hashed_password = _hash_password(password)
    if user.get('password') != hashed_password:
        return {"success": False, "message": "密码错误", "data": {}}
    
    # 移除密码字段后返回用户信息
    user_info = {k: v for k, v in user.items() if k != 'password'}
    
    return {
        "success": True,
        "message": "登录成功",
        "data": user_info
    }


# 从 token_utils 导入并导出
from core.userinfo.login.token_utils import (
    generate_token,
    verify_token,
    token_required,
    get_current_user,
    set_auth_cookie,
    clear_auth_cookie,
    get_token_from_cookie,
)

# 导出主要接口
__all__ = [
    "registerUser",
    "loginUser",
    "generate_token",
    "verify_token",
    "token_required",
    "get_current_user",
    "set_auth_cookie",
    "clear_auth_cookie",
    "get_token_from_cookie",
]
