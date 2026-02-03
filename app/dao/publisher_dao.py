"""
出版社DAO
"""
from app.dao.base_dao import BaseDAO
from app.models.publisher import Publisher


class PublisherDAO(BaseDAO):
    """出版社数据访问对象"""
    
    def __init__(self):
        super().__init__(Publisher)
    
    def get_by_name(self, name):
        """根据名称查询"""
        return self.model.query.filter_by(publisher_name=name).first()
    
    def search_by_keyword(self, keyword, page=1, per_page=20):
        """
        关键字搜索
        :param keyword: 搜索关键字
        :param page: 页码
        :param per_page: 每页数量
        :return: (items, total)
        """
        query = self.model.query.filter(
            self.model.publisher_name.like(f'%{keyword}%')
        )
        total = query.count()
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        return items, total
    
    def get_active_publishers(self):
        """获取所有启用的出版社"""
        return self.model.query.filter_by(status=1).order_by(
            self.model.publisher_name
        ).all()

