"""
库存模型
"""
from app.extensions import db
from app.models.base import BaseModel


class Inventory(BaseModel):
    """教材库存表"""
    
    __tablename__ = 'inventory'
    
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='库存ID')
    textbook_id = db.Column(db.Integer, db.ForeignKey('textbook.textbook_id'), nullable=False, unique=True, comment='教材ID')
    current_quantity = db.Column(db.Integer, default=0, comment='当前库存数量')
    total_in_quantity = db.Column(db.Integer, default=0, comment='累计入库数量')
    total_out_quantity = db.Column(db.Integer, default=0, comment='累计出库数量')
    min_quantity = db.Column(db.Integer, default=10, comment='最低库存预警值')
    max_quantity = db.Column(db.Integer, default=1000, comment='最高库存预警值')
    last_in_date = db.Column(db.Date, comment='最后入库日期')
    last_out_date = db.Column(db.Date, comment='最后出库日期')
    
    def __repr__(self):
        return f'<Inventory textbook_id={self.textbook_id} quantity={self.current_quantity}>'
    
    def to_dict(self, include_relations=False):
        """转换为字典"""
        data = super().to_dict()
        
        # 转换日期
        if self.last_in_date:
            data['last_in_date'] = self.last_in_date.strftime('%Y-%m-%d')
        if self.last_out_date:
            data['last_out_date'] = self.last_out_date.strftime('%Y-%m-%d')
        
        # 计算库存状态
        if self.current_quantity < self.min_quantity:
            data['inventory_status'] = '库存不足'
        elif self.current_quantity > self.max_quantity:
            data['inventory_status'] = '库存过多'
        else:
            data['inventory_status'] = '正常'
        
        # 包含关联信息
        if include_relations and self.textbook:
            data['textbook_name'] = self.textbook.textbook_name
            data['isbn'] = self.textbook.isbn
        
        return data

