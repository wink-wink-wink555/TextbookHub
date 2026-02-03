"""
教材类型模型
"""
from app.extensions import db
from app.models.base import BaseModel


class TextbookType(BaseModel):
    """教材类型表"""
    
    __tablename__ = 'textbook_type'
    
    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='类型ID')
    type_name = db.Column(db.String(50), nullable=False, unique=True, comment='类型名称')
    type_code = db.Column(db.String(20), nullable=False, unique=True, comment='类型编码')
    description = db.Column(db.Text, comment='类型描述')
    parent_id = db.Column(db.Integer, db.ForeignKey('textbook_type.type_id'), comment='父类型ID')
    status = db.Column(db.SmallInteger, default=1, comment='状态：1-正常，0-停用')
    
    # 关系
    textbooks = db.relationship('Textbook', backref='textbook_type', lazy='dynamic')
    children = db.relationship('TextbookType', backref=db.backref('parent', remote_side=[type_id]))
    
    def __repr__(self):
        return f'<TextbookType {self.type_name}>'
    
    def to_dict(self, include_children=False, include_textbooks=False):
        """转换为字典"""
        data = super().to_dict()
        if include_children and self.children:
            data['children'] = [child.to_dict() for child in self.children]
        if include_textbooks:
            data['textbooks_count'] = self.textbooks.count()
        return data

