"""
认证服务
"""
from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token
from app.dao.user_dao import UserDAO
from app.utils.exceptions import AuthException, ValidationException


class AuthService:
    """认证服务类"""
    
    def __init__(self):
        self.user_dao = UserDAO()
    
    def login(self, username, password):
        """
        用户登录
        :param username: 用户名
        :param password: 密码
        :return: 包含token的字典
        """
        # 查找用户
        user = self.user_dao.get_by_username(username)
        if not user:
            raise AuthException('用户名或密码错误')
        
        # 检查用户状态
        if user.status != 1:
            raise AuthException('账号已被停用')
        
        # 验证密码
        if not user.check_password(password):
            raise AuthException('用户名或密码错误')
        
        # 更新最后登录时间
        user.last_login = datetime.now()
        self.user_dao.update(user.user_id, {'last_login': user.last_login})
        
        # 生成JWT Token (identity使用user_id，additional_claims存储其他信息)
        identity = str(user.user_id)
        additional_claims = {
            'username': user.username,
            'role': user.role,
            'real_name': user.real_name
        }
        access_token = create_access_token(identity=identity, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }
    
    def register(self, username, password, real_name=None, role='普通用户', 
                 department=None, email=None, phone=None):
        """
        用户注册
        :return: 用户信息
        """
        # 检查用户名是否已存在
        if self.user_dao.get_by_username(username):
            raise ValidationException('用户名已存在')
        
        # 创建用户
        from app.models.user import User
        user = User()
        user.username = username
        user.set_password(password)
        user.real_name = real_name
        user.role = role
        user.department = department
        user.email = email
        user.phone = phone
        
        user = self.user_dao.create(user.to_dict(exclude_password=False))
        return user.to_dict()

