"""
UserInfo 模块 - 提供用户信息的 CRUD 操作接口

使用方法:
    from core.userinfo.user_service import addUser, updateUser, deleteUser, getUser
    
    # 添加用户
    addUser(username="张三", email="zhangsan@example.com", phone="13800138000")
    
    # 获取用户
    user = getUser(user_id=1)
    
    # 更新用户
    updateUser(user_id=1, username="李四")
    
    # 删除用户
    deleteUser(user_id=1)
"""

from typing import Optional, Any
from db_config import Database


def addUser(
    username: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs: Any
) -> bool:
    """
    添加新用户到 userinfo 表
    
    Args:
        username: 用户名（必填）
        email: 邮箱（可选）
        phone: 电话（可选）
        password: 密码（可选，建议加密存储）
        **kwargs: 其他自定义字段
        
    Returns:
        bool: 添加成功返回 True，失败返回 False
        
    Example:
        >>> addUser(username="张三", email="zhangsan@example.com", phone="13800138000")
        True
    """
    with Database() as db:
        # 构建动态字段
        fields = ["username"]
        values = [username]
        placeholders = ["%s"]
        
        if email is not None:
            fields.append("email")
            values.append(email)
            placeholders.append("%s")
            
        if phone is not None:
            fields.append("phone")
            values.append(phone)
            placeholders.append("%s")
            
        if password is not None:
            fields.append("password")
            values.append(password)
            placeholders.append("%s")
        
        # 处理额外的自定义字段
        for key, value in kwargs.items():
            fields.append(key)
            values.append(value)
            placeholders.append("%s")
        
        query = f"""
            INSERT INTO userinfo ({', '.join(fields)})
            VALUES ({', '.join(placeholders)})
        """
        
        return db.execute_update(query, tuple(values))


def updateUser(
    user_id: str,
    username: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs: Any
) -> bool:
    """
    更新 userinfo 表中的用户信息
    
    Args:
        user_id: 用户ID（必填，UUID）
        username: 新用户名（可选）
        email: 新邮箱（可选）
        phone: 新电话（可选）
        password: 新密码（可选）
        **kwargs: 其他需要更新的自定义字段
        
    Returns:
        bool: 更新成功返回 True，失败返回 False
        
    Example:
        >>> updateUser(user_id=1, username="李四", email="lisi@example.com")
        True
    """
    with Database() as db:
        # 构建更新字段
        update_fields: list[Any] = []
        values: list[Any] = []
        
        if username is not None:
            update_fields.append("username = %s")
            values.append(username)
            
        if email is not None:
            update_fields.append("email = %s")
            values.append(email)
            
        if phone is not None:
            update_fields.append("phone = %s")
            values.append(phone)
            
        if password is not None:
            update_fields.append("password = %s")
            values.append(password)
        
        # 处理额外的自定义字段
        for key, value in kwargs.items():
            update_fields.append(f"{key} = %s")
            values.append(value)
        
        if not update_fields:
            print("[DEBUG] 没有要更新的字段")
            return False
        
        # 添加 WHERE 条件的 user_id
        values.append(user_id)
        
        query = f"""
            UPDATE userinfo
            SET {', '.join(update_fields)}
            WHERE id = %s
        """
        
        return db.execute_update(query, tuple(values))


def deleteUser(user_id: str) -> bool:
    """
    从 userinfo 表删除用户
    
    Args:
        user_id: 要删除的用户ID（UUID）
        
    Returns:
        bool: 删除成功返回 True，失败返回 False
        
    Example:
        >>> deleteUser(user_id=1)
        True
    """
    with Database() as db:
        query = "DELETE FROM userinfo WHERE id = %s"
        return db.execute_update(query, (user_id,))


def getUser(
    user_id: Optional[str] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None
) -> Optional[dict]:
    """
    从 userinfo 表获取用户信息
    
    支持通过 user_id、username、email 或 phone 查询用户。
    如果提供多个参数，将使用 AND 组合条件。
    
    Args:
        user_id: 用户ID（可选）
        username: 用户名（可选）
        email: 邮箱（可选）
        phone: 电话（可选）
        
    Returns:
        dict: 用户信息的字典，未找到返回 None
        
    Example:
        >>> getUser(user_id=1)
        {'id': 1, 'username': '张三', 'email': 'zhangsan@example.com', ...}
        
        >>> getUser(email="zhangsan@example.com")
        {'id': 1, 'username': '张三', 'email': 'zhangsan@example.com', ...}
    """
    with Database() as db:
        # 构建 WHERE 条件
        conditions = []
        values = []
        
        if user_id is not None:
            conditions.append("id = %s")
            values.append(user_id)
            
        if username is not None:
            conditions.append("username = %s")
            values.append(username)
            
        if email is not None:
            conditions.append("email = %s")
            values.append(email)
            
        if phone is not None:
            conditions.append("phone = %s")
            values.append(phone)
        
        if not conditions:
            print("[DEBUG] 请至少提供一个查询条件")
            return None
        
        query = f"SELECT * FROM userinfo WHERE {' AND '.join(conditions)} LIMIT 1"
        result = db.execute_query(query, tuple(values))
        
        if result and len(result) > 0:
            return dict(result[0])
        return None


def getAllUsers(
    limit: int = 100,
    offset: int = 0
) -> list[dict]:
    """
    获取所有用户列表（带分页）
    
    Args:
        limit: 返回的最大记录数，默认 100
        offset: 跳过的记录数，默认 0
        
    Returns:
        list[dict]: 用户列表
        
    Example:
        >>> getAllUsers(limit=10, offset=0)
        [{'id': 1, 'username': '张三', ...}, {'id': 2, 'username': '李四', ...}]
    """
    with Database() as db:
        query = "SELECT * FROM userinfo ORDER BY id LIMIT %s OFFSET %s"
        result = db.execute_query(query, (limit, offset))
        
        if result:
            return [dict(row) for row in result]
        return []


# 导出主要接口
__all__ = [
    "addUser",
    "updateUser", 
    "deleteUser",
    "getUser",
    "getAllUsers"
]
