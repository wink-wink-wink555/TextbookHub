"""
入库服务
"""
from sqlalchemy import text
from app.dao.stock_in_dao import StockInDAO
from app.dao.purchase_order_dao import PurchaseOrderDAO
from app.extensions import db
from app.utils.exceptions import BusinessException


class StockInService:
    """入库服务类"""
    
    def __init__(self):
        self.stock_in_dao = StockInDAO()
        self.purchase_dao = PurchaseOrderDAO()
    
    def generate_stock_in_no(self):
        """生成入库单号"""
        # 调用存储过程生成入库单号
        db.session.execute(text("CALL sp_generate_stock_in_no(@stock_in_no)"))
        result = db.session.execute(text("SELECT @stock_in_no"))
        stock_in_no = result.scalar()
        return stock_in_no
    
    def get_stock_in_list(self, page=1, per_page=20, keyword=None, 
                          start_date=None, end_date=None):
        """获取入库列表"""
        items, total = self.stock_in_dao.search(
            keyword=keyword,
            start_date=start_date,
            end_date=end_date,
            page=page,
            per_page=per_page
        )
        
        result = [item.to_dict(include_relations=True) for item in items]
        return result, total
    
    def get_stock_in_detail(self, stock_in_id):
        """获取入库详情"""
        stock_in = self.stock_in_dao.get_by_id(stock_in_id)
        return stock_in.to_dict(include_relations=True)
    
    def create_stock_in(self, data):
        """
        创建入库单
        注意：触发器会自动更新库存和订单状态
        """
        # 验证订单是否存在
        order = self.purchase_dao.get_by_id(data['order_id'])
        if not order:
            raise BusinessException('订单不存在')
        
        if order.order_status == '已取消':
            raise BusinessException('订单已取消，不能入库')
        
        # 验证入库数量
        remaining = order.order_quantity - order.arrived_quantity
        if data['actual_quantity'] > remaining:
            raise BusinessException(f'入库数量超出订单剩余数量（剩余：{remaining}）')
        
        # 生成入库单号
        data['stock_in_no'] = self.generate_stock_in_no()
        
        # 创建入库单（触发器会自动更新库存）
        stock_in = self.stock_in_dao.create(data)
        db.session.commit()
        
        return stock_in.to_dict(include_relations=True)
    
    def update_stock_in(self, stock_in_id, data):
        """更新入库单"""
        stock_in = self.stock_in_dao.update(stock_in_id, data)
        db.session.commit()
        return stock_in.to_dict(include_relations=True)
    
    def delete_stock_in(self, stock_in_id):
        """
        删除入库单
        注意：触发器会自动回退库存和订单数量
        """
        try:
            self.stock_in_dao.delete(stock_in_id, soft=False)
            db.session.commit()
            return {'message': '删除成功'}
        except Exception as e:
            db.session.rollback()
            # 如果触发器抛出错误（如库存不足），会在这里捕获
            raise BusinessException(f'删除失败：{str(e)}')
