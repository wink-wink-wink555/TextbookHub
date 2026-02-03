"""
教材模型
"""
from app.extensions import db
from app.models.base import BaseModel
from datetime import datetime


class Textbook(BaseModel):
    """教材信息表"""
    
    __tablename__ = 'textbook'
    
    textbook_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='教材ID')
    isbn = db.Column(db.String(20), nullable=False, unique=True, comment='国际标准书号')
    textbook_name = db.Column(db.String(200), nullable=False, comment='教材名称')
    author = db.Column(db.String(100), comment='作者')
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.publisher_id'), nullable=False, comment='出版社ID')
    type_id = db.Column(db.Integer, db.ForeignKey('textbook_type.type_id'), nullable=False, comment='教材类型ID')
    edition = db.Column(db.String(20), comment='版次')
    publication_date = db.Column(db.Date, comment='出版日期')
    price = db.Column(db.Numeric(10, 2), nullable=False, comment='单价')
    description = db.Column(db.Text, comment='教材描述')
    status = db.Column(db.SmallInteger, default=1, comment='状态：1-正常，0-停用')
    
    # 关系
    purchase_orders = db.relationship('PurchaseOrder', backref='textbook', lazy='dynamic')
    stock_ins = db.relationship('StockIn', backref='textbook', lazy='dynamic')
    # requisitions = db.relationship('Requisition', backref='textbook', lazy='dynamic')  # 已移除领用功能
    inventory = db.relationship('Inventory', backref='textbook', uselist=False)
    
    def __repr__(self):
        return f'<Textbook {self.textbook_name}>'
    
    def to_dict(self, include_relations=False):
        """转换为字典"""
        data = super().to_dict()
        # 转换价格为float
        if self.price:
            data['price'] = float(self.price)
        # 转换出版日期
        if self.publication_date:
            data['publication_date'] = self.publication_date.strftime('%Y-%m-%d')
        
        # 包含关联信息
        if include_relations:
            if self.publisher:
                data['publisher_name'] = self.publisher.publisher_name
            if self.textbook_type:
                data['type_name'] = self.textbook_type.type_name
            if self.inventory:
                data['current_quantity'] = self.inventory.current_quantity
        
        return data

