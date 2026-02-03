"""
自定义装饰器
"""
from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.utils.exceptions import PermissionException, AuthException
from app.utils.response import error_response


def permission_required(roles=None):
    """
    权限验证装饰器
    :param roles: 允许的角色列表
    """
    if roles is None:
        roles = []
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 验证JWT
            verify_jwt_in_request()
            
            # 获取当前用户信息（包含additional_claims）
            current_user = get_jwt()
            
            if not current_user:
                raise AuthException('用户未登录')
            
            # 检查角色权限
            if roles and current_user.get('role') not in roles:
                raise PermissionException(f'需要以下角色之一：{", ".join(roles)}')
            
            return f(*args, **kwargs)
        
        return wrapper
    
    return decorator


def admin_required(f):
    """管理员权限装饰器"""
    return permission_required(['管理员'])(f)


def warehouse_required(f):
    """仓库管理员及以上权限装饰器"""
    return permission_required(['管理员', '仓库管理员'])(f)


def teacher_required(f):
    """教师及以上权限装饰器"""
    return permission_required(['管理员', '仓库管理员', '教师'])(f)


def validate_request(schema_class):
    """
    请求数据验证装饰器
    :param schema_class: Marshmallow Schema类
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            schema = schema_class()
            try:
                data = schema.load(request.get_json())
                request.validated_data = data
            except Exception as e:
                return error_response(
                    message='请求数据验证失败',
                    code=400,
                    errors=str(e)
                )
            return f(*args, **kwargs)
        
        return wrapper
    
    return decorator


def get_current_user_info():
    """
    获取当前登录用户信息
    :return: 用户信息字典
    """
    try:
        verify_jwt_in_request()
        return get_jwt()
    except:
        return None


def is_admin_or_warehouse():
    """检查当前用户是否为管理员或仓库管理员"""
    user = get_current_user_info()
    if not user:
        return False
    return user.get('role') in ['管理员', '仓库管理员']


def can_manage_basic_data():
    """检查当前用户是否可以管理基础数据（教材、出版社等）"""
    user = get_current_user_info()
    if not user:
        return False
    return user.get('role') == '管理员'

