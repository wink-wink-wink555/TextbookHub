"""
入库模型
"""
from app.extensions import db
from app.models.base import BaseModel


class StockIn(BaseModel):
    """教材入库表"""
    
    __tablename__ = 'stock_in'
    
    stock_in_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='入库ID')
    stock_in_no = db.Column(db.String(50), nullable=False, unique=True, comment='入库单号')
    order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.order_id'), nullable=False, comment='订单ID')
    textbook_id = db.Column(db.Integer, db.ForeignKey('textbook.textbook_id'), nullable=False, comment='教材ID')
    stock_in_quantity = db.Column(db.Integer, nullable=False, comment='入库数量')
    stock_in_date = db.Column(db.Date, nullable=False, comment='入库日期')
    warehouse_person = db.Column(db.String(50), comment='仓库管理员')
    quality_status = db.Column(
        db.Enum('合格', '部分合格', '不合格'),
        default='合格',
        comment='质量状态'
    )
    actual_quantity = db.Column(db.Integer, nullable=False, comment='实际入库数量')
    remarks = db.Column(db.Text, comment='备注')
    
    def __repr__(self):
        return f'<StockIn {self.stock_in_no}>'
    
    def to_dict(self, include_relations=False):
        """转换为字典"""
        data = super().to_dict()
        
        # 转换日期
        if self.stock_in_date:
            data['stock_in_date'] = self.stock_in_date.strftime('%Y-%m-%d')
        
        # 包含关联信息
        if include_relations:
            if self.textbook:
                data['textbook_name'] = self.textbook.textbook_name
                data['isbn'] = self.textbook.isbn
            if self.order:
                data['order_no'] = self.order.order_no
        
        return data

