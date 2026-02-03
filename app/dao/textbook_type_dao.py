"""
教材类型DAO
"""
from app.dao.base_dao import BaseDAO
from app.models.textbook_type import TextbookType


class TextbookTypeDAO(BaseDAO):
    """教材类型数据访问对象"""
    
    def __init__(self):
        super().__init__(TextbookType)
    
    def get_by_code(self, code):
        """根据类型编码查询"""
        return self.model.query.filter_by(type_code=code).first()
    
    def get_root_types(self):
        """获取所有根类型（无父类型）"""
        return self.model.query.filter_by(parent_id=None, status=1).all()
    
    def get_children(self, parent_id):
        """获取子类型"""
        return self.model.query.filter_by(parent_id=parent_id, status=1).all()
    
    def get_tree(self):
        """获取树形结构"""
        root_types = self.get_root_types()
        tree = []
        for root in root_types:
            node = root.to_dict(include_children=True)
            tree.append(node)
        return tree
    
    def get_active_types(self):
        """获取所有启用的类型"""
        return self.model.query.filter_by(status=1).order_by(
            self.model.type_code
        ).all()

