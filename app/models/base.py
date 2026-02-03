"""
基础模型类
"""
from datetime import datetime
from app.extensions import db


class BaseModel(db.Model):
    """基础模型类，包含公共字段"""
    
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment='更新时间'
    )
    
    def to_dict(self, exclude=None):
        """
        将模型转换为字典
        :param exclude: 需要排除的字段列表
        :return: 字典
        """
        if exclude is None:
            exclude = []
        
        data = {}
        for column in self.__table__.columns:
            if column.name not in exclude:
                value = getattr(self, column.name)
                # 处理日期时间类型
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                data[column.name] = value
        return data
    
    def save(self):
        """保存到数据库"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """从数据库删除"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        """根据ID查询"""
        return cls.query.get(id)

