"""
DAO基类
"""
from app.extensions import db
from app.utils.exceptions import DatabaseException, NotFoundException


class BaseDAO:
    """DAO基类，提供通用CRUD操作"""
    
    def __init__(self, model):
        self.model = model
    
    def get_by_id(self, id):
        """
        根据ID查询
        :param id: 主键ID
        :return: 模型实例
        """
        try:
            instance = self.model.query.get(id)
            if not instance:
                raise NotFoundException(f'{self.model.__name__}不存在')
            return instance
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f'查询失败: {str(e)}')
    
    def get_all(self, filters=None, order_by=None):
        """
        查询所有记录
        :param filters: 过滤条件
        :param order_by: 排序字段
        :return: 查询结果列表
        """
        try:
            query = self.model.query
            
            # 应用过滤条件
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        query = query.filter(getattr(self.model, key) == value)
            
            # 应用排序
            if order_by:
                if isinstance(order_by, str):
                    query = query.order_by(getattr(self.model, order_by))
                elif isinstance(order_by, list):
                    for field in order_by:
                        query = query.order_by(getattr(self.model, field))
            
            return query.all()
        except Exception as e:
            raise DatabaseException(f'查询失败: {str(e)}')
    
    def paginate(self, page=1, per_page=20, filters=None, order_by=None):
        """
        分页查询
        :param page: 页码
        :param per_page: 每页数量
        :param filters: 过滤条件
        :param order_by: 排序字段
        :return: (items, total)
        """
        try:
            query = self.model.query
            
            # 应用过滤条件
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key) and value is not None:
                        if isinstance(value, list):
                            query = query.filter(getattr(self.model, key).in_(value))
                        else:
                            query = query.filter(getattr(self.model, key) == value)
            
            # 应用排序
            if order_by:
                if isinstance(order_by, str):
                    if order_by.startswith('-'):
                        # 降序
                        query = query.order_by(getattr(self.model, order_by[1:]).desc())
                    else:
                        # 升序
                        query = query.order_by(getattr(self.model, order_by))
            
            # 获取总数
            total = query.count()
            
            # 分页
            items = query.limit(per_page).offset((page - 1) * per_page).all()
            
            return items, total
        except Exception as e:
            raise DatabaseException(f'分页查询失败: {str(e)}')
    
    def create(self, data):
        """
        创建记录
        :param data: 数据字典
        :return: 创建的实例
        """
        try:
            instance = self.model(**data)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(f'创建失败: {str(e)}')
    
    def update(self, id, data):
        """
        更新记录
        :param id: 主键ID
        :param data: 更新数据字典
        :return: 更新后的实例
        """
        try:
            instance = self.get_by_id(id)
            for key, value in data.items():
                if hasattr(instance, key) and value is not None:
                    setattr(instance, key, value)
            db.session.commit()
            return instance
        except NotFoundException:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(f'更新失败: {str(e)}')
    
    def delete(self, id, soft=True):
        """
        删除记录
        :param id: 主键ID
        :param soft: 是否软删除
        :return: None
        """
        try:
            instance = self.get_by_id(id)
            if soft and hasattr(instance, 'status'):
                # 软删除
                instance.status = 0
                db.session.commit()
            else:
                # 硬删除
                db.session.delete(instance)
                db.session.commit()
        except NotFoundException:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(f'删除失败: {str(e)}')
    
    def count(self, filters=None):
        """
        统计数量
        :param filters: 过滤条件
        :return: 数量
        """
        try:
            query = self.model.query
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        query = query.filter(getattr(self.model, key) == value)
            return query.count()
        except Exception as e:
            raise DatabaseException(f'统计失败: {str(e)}')
    
    def exists(self, filters):
        """
        检查记录是否存在
        :param filters: 过滤条件
        :return: 是否存在
        """
        try:
            query = self.model.query
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
            return query.first() is not None
        except Exception as e:
            raise DatabaseException(f'检查失败: {str(e)}')

