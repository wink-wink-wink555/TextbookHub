"""
出版社模型
"""
from app.extensions import db
from app.models.base import BaseModel


class Publisher(BaseModel):
    """出版社信息表"""
    
    __tablename__ = 'publisher'
    
    publisher_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='出版社ID')
    publisher_name = db.Column(db.String(100), nullable=False, unique=True, comment='出版社名称')
    contact_person = db.Column(db.String(50), comment='联系人')
    contact_phone = db.Column(db.String(20), comment='联系电话')
    address = db.Column(db.String(200), comment='地址')
    email = db.Column(db.String(100), comment='邮箱')
    status = db.Column(db.SmallInteger, default=1, comment='状态：1-正常，0-停用')
    
    # 关系
    textbooks = db.relationship('Textbook', backref='publisher', lazy='dynamic')
    
    def __repr__(self):
        return f'<Publisher {self.publisher_name}>'
    
    def to_dict(self, include_textbooks=False):
        """转换为字典"""
        data = super().to_dict()
        if include_textbooks:
            data['textbooks_count'] = self.textbooks.count()
        return data

