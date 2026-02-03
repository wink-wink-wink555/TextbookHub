"""
用户模型
"""
from app.extensions import db
from app.models.base import BaseModel
from app.utils.helpers import hash_password, verify_password


class User(BaseModel):
    """系统用户表"""
    
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(50), nullable=False, unique=True, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='密码（加密存储）')
    real_name = db.Column(db.String(50), comment='真实姓名')
    role = db.Column(
        db.Enum('管理员', '仓库管理员', '教师', '普通用户'),
        default='普通用户',
        comment='用户角色'
    )
    department = db.Column(db.String(100), comment='所属部门')
    email = db.Column(db.String(100), comment='邮箱')
    phone = db.Column(db.String(20), comment='电话')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    status = db.Column(db.SmallInteger, default=1, comment='状态：1-正常，0-停用')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """设置密码（加密）"""
        self.password = hash_password(password)
    
    def check_password(self, password):
        """验证密码（明文比对）"""
        return password == self.password
    
    def to_dict(self, exclude_password=True):
        """转换为字典"""
        exclude_fields = ['password'] if exclude_password else []
        data = super().to_dict(exclude=exclude_fields)
        
        # 转换最后登录时间
        if self.last_login:
            data['last_login'] = self.last_login.strftime('%Y-%m-%d %H:%M:%S')
        
        return data
    
    def to_jwt_identity(self):
        """生成JWT身份信息"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role,
            'real_name': self.real_name
        }

