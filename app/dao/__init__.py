"""
数据访问层模块
"""
from app.dao.base_dao import BaseDAO
from app.dao.publisher_dao import PublisherDAO
from app.dao.textbook_type_dao import TextbookTypeDAO
from app.dao.textbook_dao import TextbookDAO
from app.dao.purchase_order_dao import PurchaseOrderDAO
from app.dao.stock_in_dao import StockInDAO
# from app.dao.requisition_dao import RequisitionDAO  # 已移除领用功能
from app.dao.inventory_dao import InventoryDAO
from app.dao.user_dao import UserDAO

__all__ = [
    'BaseDAO',
    'PublisherDAO',
    'TextbookTypeDAO',
    'TextbookDAO',
    'PurchaseOrderDAO',
    'StockInDAO',
    # 'RequisitionDAO',  # 已移除领用功能
    'InventoryDAO',
    'UserDAO'
]

