"""
订购DAO
"""
from app.dao.base_dao import BaseDAO
from app.models.purchase_order import PurchaseOrder
from app.extensions import db


class PurchaseOrderDAO(BaseDAO):
    """订购数据访问对象"""
    
    def __init__(self):
        super().__init__(PurchaseOrder)
    
    def get_by_order_no(self, order_no):
        """根据订单号查询"""
        return self.model.query.filter_by(order_no=order_no).first()
    
    def get_by_status(self, status, page=1, per_page=20):
        """
        按状态查询
        :param status: 订单状态
        :param page: 页码
        :param per_page: 每页数量
        :return: (items, total)
        """
        query = self.model.query.filter_by(order_status=status)
        total = query.count()
        items = query.order_by(
            self.model.order_date.desc()
        ).limit(per_page).offset((page - 1) * per_page).all()
        return items, total
    
    def get_by_textbook(self, textbook_id):
        """获取指定教材的所有订单"""
        return self.model.query.filter_by(textbook_id=textbook_id).order_by(
            self.model.order_date.desc()
        ).all()
    
    def get_pending_orders(self):
        """获取待处理的订单（待审核、已审核、已订购）"""
        return self.model.query.filter(
            self.model.order_status.in_(['待审核', '已审核', '已订购', '部分到货'])
        ).order_by(self.model.order_date).all()
    
    def search(self, keyword=None, status=None, start_date=None, end_date=None, 
               order_person=None, current_username=None, allowed_roles=None, 
               page=1, per_page=20):
        """
        多条件搜索
        :param keyword: 搜索关键字
        :param status: 订单状态
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param order_person: 订购人（用于数据权限过滤）
        :param current_username: 当前用户名（用于教师权限过滤）
        :param allowed_roles: 允许查看的角色列表（用于教师权限过滤）
        :param page: 页码
        :param per_page: 每页数量
        :return: (items, total)
        """
        query = self.model.query
        
        if keyword:
            query = query.filter(
                db.or_(
                    self.model.order_no.like(f'%{keyword}%'),
                    self.model.order_person.like(f'%{keyword}%')
                )
            )
        
        if status:
            query = query.filter_by(order_status=status)
        
        if start_date:
            query = query.filter(self.model.order_date >= start_date)
        
        if end_date:
            query = query.filter(self.model.order_date <= end_date)
        
        # 数据权限过滤：按订购人过滤
        if order_person:
            query = query.filter_by(order_person=order_person)
        
        # 教师特殊权限：查看自己和普通用户的订单
        if current_username and allowed_roles:
            # 教师可以查看order_person是自己或普通用户的订单
            # 需要通过订购人的用户名查询用户角色
            from app.models.user import User
            
            # 获取普通用户的用户名列表
            normal_users = db.session.query(User.username).filter_by(role='普通用户', status=1).all()
            normal_usernames = [u[0] for u in normal_users]
            
            # 过滤条件：订购人是当前用户或者是普通用户
            query = query.filter(
                db.or_(
                    self.model.order_person == current_username,
                    self.model.order_person.in_(normal_usernames)
                )
            )
        
        total = query.count()
        items = query.order_by(
            self.model.order_date.desc()
        ).limit(per_page).offset((page - 1) * per_page).all()
        return items, total

