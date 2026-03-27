"""
JWT Token 工具模块
提供 token 生成、验证和 cookie 管理功能
"""

import jwt
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from typing import Optional, Callable, Any

# JWT 配置
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24  # Token 过期时间 24 小时


def generate_token(user_id: str, username: str) -> str:
    """
    生成 JWT Token
    
    Args:
        user_id: 用户ID (UUID)
        username: 用户名
        
    Returns:
        str: JWT Token 字符串
    """
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        'user_id': user_id,
        'username': username,
        'iat': now,  # 签发时间
        'exp': now + timedelta(hours=JWT_EXPIRATION_HOURS),  # 过期时间
        'type': 'access'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> tuple[bool, Optional[dict[str, Any]], Optional[str]]:
    """
    验证 JWT Token
    
    Args:
        token: JWT Token 字符串
        
    Returns:
        tuple[bool, Optional[dict], Optional[str]]: (是否有效, payload数据, 错误信息)
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True, payload, None
    except jwt.ExpiredSignatureError:
        return False, None, 'token已过期'
    except jwt.InvalidTokenError:
        return False, None, 'token无效'


def get_token_from_cookie() -> Optional[str]:
    """
    从 cookie 中获取 token
    
    Returns:
        Optional[str]: token 字符串或 None
    """
    from flask import request
    return request.cookies.get('auth_token')


def token_required(f: Callable[..., Any]) -> Callable[..., Any]:
    """
    Token 验证装饰器
    用于保护需要登录才能访问的接口
    
    使用方法:
        @token_required
        def protected_route():
            return jsonify({"message": "success"})
    """
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        token = get_token_from_cookie()
        
        if not token:
            return jsonify({
                'success': False,
                'message': '请先登录'
            }), 401
        
        is_valid, payload, error = verify_token(token)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'message': f'登录{error}，请重新登录'
            }), 401
        
        # 将用户信息注入到请求上下文中
        setattr(request, 'current_user', payload)
        return f(*args, **kwargs)
    
    return decorated


def get_current_user() -> Optional[dict[str, Any]]:
    """
    获取当前登录用户信息
    需要在 token_required 装饰器保护的接口中使用
    
    Returns:
        Optional[dict]: 用户信息或 None
    """
    return getattr(request, 'current_user', None)


def set_auth_cookie(response, token: str) -> None:
    """
    设置认证 cookie
    
    Args:
        response: Flask Response 对象
        token: JWT Token
    """
    import os
    
    # 计算过期时间（秒）
    max_age = JWT_EXPIRATION_HOURS * 3600
    
    # 检测是否为开发环境
    is_dev = os.getenv('FLASK_ENV') == 'development' or os.getenv('DEBUG') == 'True'
    
    # 开发环境使用 Lax，因为 None 需要 secure=True（需要 HTTPS）
    # 由于使用了 Vite 代理，前后端在同域下，Lax 是安全的
    samesite = 'Lax' if is_dev else 'Lax'
    secure = not is_dev  # 生产环境需要 HTTPS
    
    response.set_cookie(
        'auth_token',
        token,
        max_age=max_age,
        httponly=True,
        secure=secure,
        samesite=samesite,
        path='/'
    )


def clear_auth_cookie(response) -> None:
    """
    清除认证 cookie（用于登出）
    
    Args:
        response: Flask Response 对象
    """
    import os
    
    is_dev = os.getenv('FLASK_ENV') == 'development' or os.getenv('DEBUG') == 'True'
    
    response.delete_cookie(
        'auth_token',
        path='/',
        domain=None,
        secure=not is_dev,
        samesite='Lax' if is_dev else 'Lax'
    )
