"""
订购模型
"""
from app.extensions import db
from app.models.base import BaseModel
from datetime import datetime


class PurchaseOrder(BaseModel):
    """教材订购表"""
    
    __tablename__ = 'purchase_order'
    
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='订单ID')
    order_no = db.Column(db.String(50), nullable=False, unique=True, comment='订单编号')
    textbook_id = db.Column(db.Integer, db.ForeignKey('textbook.textbook_id'), nullable=False, comment='教材ID')
    order_quantity = db.Column(db.Integer, nullable=False, comment='订购数量')
    order_date = db.Column(db.Date, nullable=False, comment='订购日期')
    expected_date = db.Column(db.Date, comment='预计到货日期')
    order_person = db.Column(db.String(50), comment='订购人')
    order_status = db.Column(
        db.Enum('待审核', '已审核', '已订购', '部分到货', '已到货', '已发放', '已取消'),
        default='待审核',
        comment='订单状态'
    )
    arrived_quantity = db.Column(db.Integer, default=0, comment='已到货数量')
    remarks = db.Column(db.Text, comment='备注')
    
    # 关系
    stock_ins = db.relationship('StockIn', backref='order', lazy='dynamic')
    
    def __repr__(self):
        return f'<PurchaseOrder {self.order_no}>'
    
    def to_dict(self, include_relations=False):
        """转换为字典"""
        data = super().to_dict()
        
        # 转换日期
        if self.order_date:
            data['order_date'] = self.order_date.strftime('%Y-%m-%d')
        if self.expected_date:
            data['expected_date'] = self.expected_date.strftime('%Y-%m-%d')
        
        # 包含关联信息
        if include_relations and self.textbook:
            data['textbook_name'] = self.textbook.textbook_name
            data['isbn'] = self.textbook.isbn
        
        return data

