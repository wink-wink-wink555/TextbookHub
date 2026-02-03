"""
认证API
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1
from app.services.auth_service import AuthService
from app.schemas.user_schema import LoginSchema, UserSchema
from app.utils.response import success_response, error_response
from marshmallow import ValidationError


auth_service = AuthService()


@api_v1.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        # 验证请求数据
        schema = LoginSchema()
        data = schema.load(request.get_json())
        
        # 执行登录
        result = auth_service.login(data['username'], data['password'])
        
        return success_response(data=result, message='登录成功')
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        # 验证请求数据
        schema = UserSchema()
        data = schema.load(request.get_json())
        
        # 执行注册
        result = auth_service.register(
            username=data['username'],
            password=data['password'],
            real_name=data.get('real_name'),
            role=data.get('role', '普通用户'),
            department=data.get('department'),
            email=data.get('email'),
            phone=data.get('phone')
        )
        
        return success_response(data=result, message='注册成功', code=201)
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/auth/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前登录用户信息"""
    try:
        current_user = get_jwt_identity()
        return success_response(data=current_user)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/auth/users', methods=['GET'])
@jwt_required()
def get_users():
    """获取用户列表（用于订购人下拉选择）"""
    try:
        from flask_jwt_extended import get_jwt
        from app.dao.user_dao import UserDAO
        
        current_user = get_jwt()
        user_role = current_user.get('role')
        # 注意：JWT的sub存储的是user_id，username在additional_claims中
        current_username = current_user.get('username')
        
        user_dao = UserDAO()
        
        # 根据角色返回不同的用户列表
        if user_role in ['管理员', '仓库管理员']:
            # 管理员和仓库管理员可以看到所有用户
            users = user_dao.get_all_users()
        elif user_role == '教师':
            # 教师可以看到自己和普通用户
            normal_users = user_dao.get_users_by_role('普通用户')
            current_user_obj = user_dao.find_by_username(current_username)
            # 确保自己在列表前面，并避免重复
            users = []
            if current_user_obj:
                users.append(current_user_obj)
            for u in normal_users:
                if u.username != current_username:  # 避免重复
                    users.append(u)
        else:
            # 普通用户只能看到自己
            current_user_obj = user_dao.find_by_username(current_username)
            users = [current_user_obj] if current_user_obj else []
        
        # 格式化返回数据
        user_list = []
        for user in users:
            if user:
                user_list.append({
                    'user_id': user.user_id,
                    'username': user.username,
                    'real_name': user.real_name,
                    'role': user.role,
                    'department': user.department
                })
        
        return success_response(data=user_list)
    except Exception as e:
        return error_response(message=str(e))

