"""
UserInfo API 路由模块
提供 RESTful API 接口供前端调用 userinfo 表的操作

API 端点:
    POST   /api/userinfo/add       - 添加用户
    PUT    /api/userinfo/update    - 更新用户
    DELETE /api/userinfo/delete    - 删除用户
    GET    /api/userinfo/get       - 获取单个用户
    GET    /api/userinfo/list      - 获取用户列表
    GET    /api/userinfo/profile   - 获取当前登录用户信息
"""

from flask import Blueprint, request, jsonify
from core.userinfo.user_service import addUser, updateUser, deleteUser, getUser, getAllUsers
from core.userinfo.login.auth_service import token_required, get_current_user
from core.response import success_response, error_response, created_response, list_response, ResponseCode

userinfo_bp = Blueprint('userinfo', __name__)


@userinfo_bp.route('/add', methods=['POST'])
def api_add_user():
    """
    添加新用户
    
    POST /api/userinfo/add
    
    Request Body:
        {
            "username": "张三",      // 必填
            "email": "zhangsan@example.com",  // 可选
            "phone": "13800138000",           // 可选
            "password": "123456"              // 可选
        }
    
    Response:
        {
            "success": true,
            "message": "用户添加成功",
            "data": true
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data:
            response, code = error_response("缺少必填字段: username", ResponseCode.BAD_REQUEST)
            return jsonify(response), code
        
        # 提取字段
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        
        # 调用业务逻辑
        success = addUser(
            username=username,
            email=email,
            phone=phone,
            password=password
        )
        
        if success:
            response, code = created_response(data=True, message="用户添加成功")
            return jsonify(response), code
        else:
            response, code = error_response("用户添加失败", ResponseCode.INTERNAL_ERROR)
            return jsonify(response), code
            
    except Exception as e:
        response, code = error_response(f"服务器错误: {str(e)}", ResponseCode.INTERNAL_ERROR)
        return jsonify(response), code


@userinfo_bp.route('/update', methods=['PUT'])
def api_update_user():
    """
    更新用户信息
    
    PUT /api/userinfo/update
    
    Request Body:
        {
            "user_id": 1,              // 必填
            "username": "李四",        // 可选
            "email": "lisi@example.com", // 可选
            "phone": "13900139000",     // 可选
            "password": "newpassword"   // 可选
        }
    
    Response:
        {
            "success": true,
            "message": "用户更新成功",
            "data": true
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            response, code = error_response("缺少必填字段: user_id", ResponseCode.BAD_REQUEST)
            return jsonify(response), code
        
        user_id = data.get('user_id')
        
        # 提取可选字段
        update_data = {}
        if 'username' in data:
            update_data['username'] = data['username']
        if 'email' in data:
            update_data['email'] = data['email']
        if 'phone' in data:
            update_data['phone'] = data['phone']
        if 'password' in data:
            update_data['password'] = data['password']
        
        if not update_data:
            response, code = error_response("至少提供一个要更新的字段", ResponseCode.BAD_REQUEST)
            return jsonify(response), code
        
        # 调用业务逻辑
        success = updateUser(user_id=user_id, **update_data)
        
        if success:
            response, code = success_response(data=True, message="用户更新成功")
            return jsonify(response), code
        else:
            response, code = error_response("用户更新失败", ResponseCode.INTERNAL_ERROR)
            return jsonify(response), code
            
    except Exception as e:
        response, code = error_response(f"服务器错误: {str(e)}", ResponseCode.INTERNAL_ERROR)
        return jsonify(response), code


@userinfo_bp.route('/delete', methods=['DELETE'])
def api_delete_user():
    """
    删除用户
    
    DELETE /api/userinfo/delete?user_id=1
    
    Query Parameters:
        user_id: 用户ID (必填)
    
    Response:
        {
            "success": true,
            "message": "用户删除成功",
            "data": true
        }
    """
    try:
        user_id = request.args.get('user_id')

        if user_id is None:
            # 尝试从 body 获取
            data = request.get_json(silent=True)
            if data and 'user_id' in data:
                user_id = data['user_id']
        
        if user_id is None:
            response, code = error_response("缺少必填参数: user_id", ResponseCode.BAD_REQUEST)
            return jsonify(response), code
        
        success = deleteUser(user_id=user_id)
        
        if success:
            response, code = success_response(data=True, message="用户删除成功")
            return jsonify(response), code
        else:
            response, code = error_response("用户删除失败", ResponseCode.INTERNAL_ERROR)
            return jsonify(response), code
            
    except Exception as e:
        response, code = error_response(f"服务器错误: {str(e)}", ResponseCode.INTERNAL_ERROR)
        return jsonify(response), code


@userinfo_bp.route('/get', methods=['GET'])
@token_required
def api_get_user():
    """
    获取单个用户信息
    
    GET /api/userinfo/get?user_id=1
    GET /api/userinfo/get?email=zhangsan@example.com
    GET /api/userinfo/get?phone=13800138000
    GET /api/userinfo/get?username=张三
    
    Query Parameters (至少提供一个):
        user_id: 用户ID
        username: 用户名
        email: 邮箱
        phone: 电话
    
    Response:
        {
            "success": true,
            "message": "获取成功",
            "data": {
                "id": 1,
                "username": "张三",
                "email": "zhangsan@example.com",
                "phone": "13800138000"
            }
        }
    """
    try:
        user_id = request.args.get('user_id')
        username = request.args.get('username')
        email = request.args.get('email')
        phone = request.args.get('phone')
        
        # 至少需要一个查询条件
        if not any([user_id, username, email, phone]):
            response, code = error_response(
                "请提供至少一个查询条件: user_id, username, email 或 phone", 
                ResponseCode.BAD_REQUEST
            )
            return jsonify(response), code
        
        user = getUser(
            user_id=user_id,
            username=username,
            email=email,
            phone=phone
        )
        
        if user:
            response, code = success_response(data=user, message="获取成功")
            return jsonify(response), code
        else:
            response, code = error_response("用户不存在", ResponseCode.NOT_FOUND)
            return jsonify(response), code
            
    except Exception as e:
        response, code = error_response(f"服务器错误: {str(e)}", ResponseCode.INTERNAL_ERROR)
        return jsonify(response), code


@userinfo_bp.route('/list', methods=['GET'])
@token_required
def api_get_all_users():
    """
    获取用户列表
    
    GET /api/userinfo/list?limit=100&offset=0
    
    Query Parameters:
        limit: 返回的最大记录数 (默认 100)
        offset: 跳过的记录数 (默认 0)
    
    Response:
        {
            "success": true,
            "message": "获取成功",
            "data": [
                {"id": 1, "username": "张三", ...},
                {"id": 2, "username": "李四", ...}
            ],
            "total": 2
        }
    """
    try:
        limit = request.args.get('limit', default=100, type=int)
        offset = request.args.get('offset', default=0, type=int)
        
        users = getAllUsers(limit=limit, offset=offset)
        
        response, code = list_response(data=users, total=len(users), message="获取成功")
        return jsonify(response), code
        
    except Exception as e:
        response, code = error_response(f"服务器错误: {str(e)}", ResponseCode.INTERNAL_ERROR)
        return jsonify(response), code


@userinfo_bp.route('/profile', methods=['GET'])
@token_required
def api_get_profile():
    """
    获取当前登录用户的详细信息
    
    GET /api/userinfo/profile
    
    Headers: Cookie: auth_token=xxx
    
    Response:
        成功 (200):
        {
            "success": true,
            "message": "获取成功",
            "data": {
                "id": 1,
                "username": "张三",
                "email": "zhangsan@example.com",
                "phone": "13800138000"
            }
        }
    """
    try:
        current_user = get_current_user()
        if not current_user:
            response, code = error_response("无法获取用户信息", ResponseCode.UNAUTHORIZED)
            return jsonify(response), code
        
        user_id = current_user.get('user_id')
        user = getUser(user_id=user_id)
        
        if user:
            # 移除密码字段
            user_info = {k: v for k, v in user.items() if k != 'password'}
            response, code = success_response(data=user_info, message="获取成功")
            return jsonify(response), code
        else:
            response, code = error_response("用户不存在", ResponseCode.NOT_FOUND)
            return jsonify(response), code
            
    except Exception as e:
        response, code = error_response(f"服务器错误: {str(e)}", ResponseCode.INTERNAL_ERROR)
        return jsonify(response), code


@userinfo_bp.route('/', methods=['GET'])
def api_info():
    """API 信息"""
    response, code = success_response(
        data={
            "name": "UserInfo API",
            "endpoints": {
                "add": {"method": "POST", "url": "/api/userinfo/add", "auth": False},
                "update": {"method": "PUT", "url": "/api/userinfo/update", "auth": False},
                "delete": {"method": "DELETE", "url": "/api/userinfo/delete", "auth": False},
                "get": {"method": "GET", "url": "/api/userinfo/get", "auth": True},
                "list": {"method": "GET", "url": "/api/userinfo/list", "auth": True},
                "profile": {"method": "GET", "url": "/api/userinfo/profile", "auth": True, "description": "获取当前登录用户信息"}
            }
        },
        message="UserInfo API 信息"
    )
    return jsonify(response), code
