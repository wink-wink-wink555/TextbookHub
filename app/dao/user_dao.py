"""
用户DAO
"""
from app.dao.base_dao import BaseDAO
from app.models.user import User


class UserDAO(BaseDAO):
    """用户数据访问对象"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_username(self, username):
        """根据用户名查询"""
        return self.model.query.filter_by(username=username).first()
    
    def find_by_username(self, username):
        """根据用户名查询（别名方法，与其他DAO保持一致）"""
        return self.get_by_username(username)
    
    def get_by_role(self, role):
        """根据角色查询所有用户"""
        return self.model.query.filter_by(role=role, status=1).all()
    
    def get_users_by_role(self, role):
        """根据角色获取用户列表（别名方法）"""
        return self.get_by_role(role)
    
    def get_active_users(self):
        """获取所有启用的用户"""
        return self.model.query.filter_by(status=1).all()
    
    def get_all_users(self):
        """获取所有用户（别名方法）"""
        return self.get_active_users()
    
    def search(self, keyword=None, role=None, department=None, 
               page=1, per_page=20):
        """
        多条件搜索
        :param keyword: 搜索关键字
        :param role: 角色
        :param department: 部门
        :param page: 页码
        :param per_page: 每页数量
        :return: (items, total)
        """
        query = self.model.query
        
        if keyword:
            from app.extensions import db
            query = query.filter(
                db.or_(
                    self.model.username.like(f'%{keyword}%'),
                    self.model.real_name.like(f'%{keyword}%')
                )
            )
        
        if role:
            query = query.filter_by(role=role)
        
        if department:
            query = query.filter_by(department=department)
        
        total = query.count()
        items = query.order_by(
            self.model.created_at.desc()
        ).limit(per_page).offset((page - 1) * per_page).all()
        return items, total

