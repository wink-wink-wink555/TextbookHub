"""
库存DAO
"""
from sqlalchemy import text
from app.dao.base_dao import BaseDAO
from app.models.inventory import Inventory
from app.extensions import db


class InventoryDAO(BaseDAO):
    """库存数据访问对象"""
    
    def __init__(self):
        super().__init__(Inventory)
    
    def get_by_textbook(self, textbook_id):
        """根据教材ID查询库存"""
        return self.model.query.filter_by(textbook_id=textbook_id).first()
    
    def get_by_textbook_id(self, textbook_id):
        """根据教材ID查询库存（别名方法）"""
        return self.get_by_textbook(textbook_id)
    
    def get_low_stock(self, page=1, per_page=20):
        """
        获取库存不足的教材
        :param page: 页码
        :param per_page: 每页数量
        :return: (items, total)
        """
        query = self.model.query.filter(
            self.model.current_quantity < self.model.min_quantity
        )
        total = query.count()
        items = query.order_by(self.model.current_quantity).limit(per_page).offset(
            (page - 1) * per_page
        ).all()
        return items, total
    
    def get_high_stock(self, page=1, per_page=20):
        """
        获取库存过多的教材
        :param page: 页码
        :param per_page: 每页数量
        :return: (items, total)
        """
        query = self.model.query.filter(
            self.model.current_quantity > self.model.max_quantity
        )
        total = query.count()
        items = query.order_by(
            self.model.current_quantity.desc()
        ).limit(per_page).offset((page - 1) * per_page).all()
        return items, total
    
    def get_warnings(self):
        """获取所有预警库存（使用视图v_inventory_warning）"""
        result = db.session.execute(text("""
            SELECT 
                textbook_id,
                isbn,
                textbook_name,
                publisher_name,
                type_name,
                current_quantity,
                min_quantity,
                max_quantity,
                warning_status
            FROM v_inventory_warning
            ORDER BY warning_level ASC, gap_quantity DESC
        """))
        rows = result.fetchall()
        return rows
    
    def get_zero_stock(self):
        """获取零库存教材"""
        return self.model.query.filter_by(current_quantity=0).all()
    
    def get_total_value(self):
        """
        计算库存总价值
        需要关联教材表查询价格
        """
        from app.models.textbook import Textbook
        result = db.session.query(
            db.func.sum(Textbook.price * Inventory.current_quantity)
        ).select_from(Inventory).join(
            Textbook, Inventory.textbook_id == Textbook.textbook_id
        ).scalar()
        return float(result) if result else 0.0

