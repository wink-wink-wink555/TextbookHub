"""
教材服务
"""
from app.dao.textbook_dao import TextbookDAO
from app.dao.inventory_dao import InventoryDAO
from app.utils.exceptions import ValidationException, NotFoundException


class TextbookService:
    """教材服务类"""
    
    def __init__(self):
        self.textbook_dao = TextbookDAO()
        self.inventory_dao = InventoryDAO()
    
    def get_textbook_list(self, page=1, per_page=20, keyword=None, 
                          publisher_id=None, type_id=None):
        """获取教材列表"""
        filters = {'status': 1}
        if publisher_id:
            filters['publisher_id'] = publisher_id
        if type_id:
            filters['type_id'] = type_id
        
        items, total = self.textbook_dao.paginate(
            page=page,
            per_page=per_page,
            filters=filters
        )
        
        result = []
        for item in items:
            data = item.to_dict(include_relations=True)
            result.append(data)
        
        return result, total
    
    def get_textbook_detail(self, textbook_id):
        """获取教材详情"""
        textbook = self.textbook_dao.get_by_id(textbook_id)
        data = textbook.to_dict(include_relations=True)
        
        # 获取库存信息
        inventory = self.inventory_dao.get_by_textbook(textbook_id)
        if inventory:
            data['inventory'] = inventory.to_dict()
        
        return data
    
    def create_textbook(self, data):
        """创建教材"""
        # 检查ISBN是否已存在
        if self.textbook_dao.get_by_isbn(data['isbn']):
            raise ValidationException('ISBN已存在')
        
        textbook = self.textbook_dao.create(data)
        return textbook.to_dict(include_relations=True)
    
    def update_textbook(self, textbook_id, data):
        """更新教材"""
        textbook = self.textbook_dao.update(textbook_id, data)
        return textbook.to_dict(include_relations=True)
    
    def delete_textbook(self, textbook_id):
        """删除教材（软删除）"""
        self.textbook_dao.delete(textbook_id, soft=True)

