"""
用户认证 API 路由模块
提供用户注册和登录的 RESTful API 接口

API 端点:
    POST /api/auth/register    - 用户注册
    POST /api/auth/login       - 用户登录
    POST /api/auth/logout      - 用户登出
    GET  /api/auth/me          - 获取当前用户信息
"""

from flask import Blueprint, request, jsonify, make_response
from core.userinfo.login.auth_service import (
    registerUser,
    loginUser,
    generate_token,
    set_auth_cookie,
    clear_auth_cookie,
    token_required,
    get_current_user,
)
from core.response import success_response, error_response, created_response, ResponseCode
from typing import List

auth_bp: Blueprint = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        
        if not data:
            response, code = error_response("请求数据不能为空", ResponseCode.BAD_REQUEST)
            return jsonify(response), code
        
        # 提取字段
        username = data.get('username', '').strip()
        email = data.get('email', '').strip() if data.get('email') else ''
        phone = data.get('phone', '').strip() if data.get('phone') else ''
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')

        # 检查必填字段
        missing_fields: List[str] = []
        if not username:
            missing_fields.append("用户名")
        if not password:
            missing_fields.append("密码")
        if not confirm_password:
            missing_fields.append("确认密码")
        
        if missing_fields:
            response, code = error_response(
                f"缺少必填字段: {', '.join(missing_fields)}", 
                ResponseCode.BAD_REQUEST
            )
            return jsonify(response), code
        
        # 调用注册逻辑
        result = registerUser(
            username=username,
            email=email,
            phone=phone,
            password=password,
            confirm_password=confirm_password
        )
        
        if result.get('success'):
            # 返回 user_id 在 data 中
            response_data = {"user_id": result.get('user_id')}
            response, code = created_response(data=response_data, message=result.get('message', '注册成功'))
            return jsonify(response), code
        else:
            response, code = error_response(result.get('message', '注册失败'), ResponseCode.BAD_REQUEST)
            return jsonify(response), code
            
    except Exception as e:
        response, code = error_response(f"服务器错误: {str(e)}", ResponseCode.INTERNAL_ERROR)
        return jsonify(response), code


@auth_bp.route('/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        
        if not data:
            response, code = error_response("请求数据不能为空", ResponseCode.BAD_REQUEST)
            return jsonify(response), code
        
        # 提取字段
        username = data.get('username', '').strip() or None
        email = data.get('email', '').strip() or None
        phone = data.get('phone', '').strip() or None
        password = data.get('password', '')
        
        # 检查密码
        if not password:
            response, code = error_response("密码不能为空", ResponseCode.BAD_REQUEST)
            return jsonify(response), code
        
        # 检查登录凭证
        if not any([username, email, phone]):
            response, code = error_response("请提供用户名、邮箱或手机号", ResponseCode.BAD_REQUEST)
            return jsonify(response), code
        
        # 调用登录逻辑
        result = loginUser(
            username=username,
            email=email,
            phone=phone,
            password=password
        )
        
        if result.get('success'):
            # 登录成功，生成 token 并设置 cookie
            user = result.get('data', {})  # 使用 data 字段
            user_id = user.get('id')
            username_value = user.get('username', '')
            
            # 生成 JWT token
            token = generate_token(user_id, username_value)
            
            # 创建响应对象 - data 直接返回 true
            response_dict, _ = success_response(data=True, message=result.get('message', '登录成功'))
            response = make_response(jsonify(response_dict), 200)
            
            # 设置认证 cookie
            set_auth_cookie(response, token)
            
            # 调试日志
            print(f"[DEBUG] 登录成功，设置 cookie: auth_token={token[:20]}...")
            
            return response
        else:
            # 根据错误信息判断状态码
            message = result.get('message', '')
            if "用户不存在" in message:
                response, code = error_response(message, ResponseCode.NOT_FOUND)
            elif "密码错误" in message:
                response, code = error_response(message, ResponseCode.UNAUTHORIZED)
            else:
                response, code = error_response(message, ResponseCode.BAD_REQUEST)
            return jsonify(response), code
                
    except Exception as e:
        response, code = error_response(f"服务器错误: {str(e)}", ResponseCode.INTERNAL_ERROR)
        return jsonify(response), code


@auth_bp.route('/logout', methods=['POST'])
def api_logout():
    try:
        response_dict, _ = success_response(data=True, message="登出成功")
        response = make_response(jsonify(response_dict), 200)
        clear_auth_cookie(response)
        return response
    except Exception as e:
        response, code = error_response(f"服务器错误: {str(e)}", ResponseCode.INTERNAL_ERROR)
        return jsonify(response), code


@auth_bp.route('/me', methods=['GET'])
@token_required
def api_get_current_user():
    user = get_current_user()
    response, code = success_response(data=user, message="获取成功")
    return jsonify(response), code


@auth_bp.route('/', methods=['GET'])
def api_info():
    response, code = success_response(
        data={
            "name": "Auth API",
            "endpoints": {
                "register": {
                    "method": "POST",
                    "url": "/api/auth/register",
                    "description": "用户注册"
                },
                "login": {
                    "method": "POST",
                    "url": "/api/auth/login",
                    "description": "用户登录"
                },
                "logout": {
                    "method": "POST",
                    "url": "/api/auth/logout",
                    "description": "用户登出"
                },
                "me": {
                    "method": "GET",
                    "url": "/api/auth/me",
                    "description": "获取当前用户信息（需登录）"
                }
            }
        },
        message="Auth API 信息"
    )
    return jsonify(response), code
