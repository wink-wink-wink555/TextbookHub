"""
教材DAO
"""
from app.dao.base_dao import BaseDAO
from app.models.textbook import Textbook
from app.extensions import db


class TextbookDAO(BaseDAO):
    """教材数据访问对象"""
    
    def __init__(self):
        super().__init__(Textbook)
    
    def get_by_isbn(self, isbn):
        """根据ISBN查询"""
        return self.model.query.filter_by(isbn=isbn).first()
    
    def search(self, keyword=None, publisher_id=None, type_id=None, 
               page=1, per_page=20):
        """
        多条件搜索
        :param keyword: 搜索关键字（教材名称或作者）
        :param publisher_id: 出版社ID
        :param type_id: 类型ID
        :param page: 页码
        :param per_page: 每页数量
        :return: (items, total)
        """
        query = self.model.query.filter_by(status=1)
        
        # 关键字搜索
        if keyword:
            query = query.filter(
                db.or_(
                    self.model.textbook_name.like(f'%{keyword}%'),
                    self.model.author.like(f'%{keyword}%'),
                    self.model.isbn.like(f'%{keyword}%')
                )
            )
        
        # 出版社筛选
        if publisher_id:
            query = query.filter_by(publisher_id=publisher_id)
        
        # 类型筛选
        if type_id:
            query = query.filter_by(type_id=type_id)
        
        total = query.count()
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        return items, total
    
    def get_by_publisher(self, publisher_id):
        """获取指定出版社的所有教材"""
        return self.model.query.filter_by(
            publisher_id=publisher_id,
            status=1
        ).all()
    
    def get_by_type(self, type_id):
        """获取指定类型的所有教材"""
        return self.model.query.filter_by(
            type_id=type_id,
            status=1
        ).all()

