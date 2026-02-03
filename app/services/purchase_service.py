"""
订购服务
"""
from datetime import datetime
from sqlalchemy import text
from app.dao.purchase_order_dao import PurchaseOrderDAO
from app.extensions import db
from app.utils.exceptions import BusinessException


class PurchaseService:
    """订购服务类"""
    
    def __init__(self):
        self.purchase_dao = PurchaseOrderDAO()
    
    def generate_order_no(self):
        """生成订单编号"""
        # 调用存储过程生成订单编号
        result = db.session.execute(
            text("CALL sp_generate_order_no(@order_no)")
        )
        order_no = db.session.execute(text("SELECT @order_no")).scalar()
        return order_no
    
    def get_order_list(self, page=1, per_page=20, status=None, 
                       start_date=None, end_date=None, keyword=None, order_person=None,
                       current_username=None, allowed_roles=None):
        """获取订单列表"""
        items, total = self.purchase_dao.search(
            keyword=keyword,
            status=status,
            start_date=start_date,
            end_date=end_date,
            order_person=order_person,
            current_username=current_username,
            allowed_roles=allowed_roles,
            page=page,
            per_page=per_page
        )
        
        result = [item.to_dict(include_relations=True) for item in items]
        return result, total
    
    def get_order_detail(self, order_id):
        """获取订单详情"""
        order = self.purchase_dao.get_by_id(order_id)
        return order.to_dict(include_relations=True)
    
    def create_order(self, data):
        """创建订单"""
        # 生成订单编号
        data['order_no'] = self.generate_order_no()
        data['order_status'] = '待审核'
        data['arrived_quantity'] = 0
        
        order = self.purchase_dao.create(data)
        return order.to_dict(include_relations=True)
    
    def update_order(self, order_id, data):
        """更新订单"""
        order = self.purchase_dao.update(order_id, data)
        return order.to_dict(include_relations=True)
    
    def approve_order(self, order_id, approver):
        """审核订单"""
        order = self.purchase_dao.get_by_id(order_id)
        
        if order.order_status != '待审核':
            raise BusinessException('订单状态不允许审核')
        
        self.purchase_dao.update(order_id, {'order_status': '已审核'})
        return {'message': '审核成功'}
    
    def cancel_order(self, order_id, reason=None):
        """取消订单"""
        order = self.purchase_dao.get_by_id(order_id)
        
        if order.order_status in ['已到货', '已取消']:
            raise BusinessException('订单状态不允许取消')
        
        self.purchase_dao.update(order_id, {
            'order_status': '已取消',
            'remarks': reason or order.remarks
        })
        return {'message': '取消成功'}

