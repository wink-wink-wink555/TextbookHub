"""
统计服务
"""
from sqlalchemy import text
from app.extensions import db
from app.dao.inventory_dao import InventoryDAO


class StatisticsService:
    """统计服务类"""
    
    def __init__(self):
        self.inventory_dao = InventoryDAO()
    
    def get_statistics_by_type(self):
        """按类型统计"""
        result = db.session.execute(text("CALL sp_statistics_by_type()"))
        rows = result.fetchall()
        
        data = []
        for row in rows:
            data.append({
                'type_id': row[0],
                'type_name': row[1],
                'type_code': row[2],
                'textbook_count': row[3],
                'order_quantity': row[4],
                'arrived_quantity': row[5],
                'issued_quantity': row[6],
                'current_quantity': row[7]
            })
        
        return data
    
    def get_statistics_by_publisher(self):
        """按出版社统计"""
        result = db.session.execute(text("CALL sp_statistics_by_publisher()"))
        rows = result.fetchall()
        
        data = []
        for row in rows:
            data.append({
                'publisher_id': row[0],
                'publisher_name': row[1],
                'textbook_count': row[2],
                'order_quantity': row[3],
                'arrived_quantity': row[4],
                'issued_quantity': row[5],
                'current_quantity': row[6]
            })
        
        return data
    
    def get_statistics_by_textbook(self, textbook_id):
        """按教材统计"""
        result = db.session.execute(
            text(f"CALL sp_statistics_by_textbook({textbook_id})")
        )
        rows = result.fetchall()
        
        if rows:
            row = rows[0]
            return {
                'textbook_id': row[0],
                'isbn': row[1],
                'textbook_name': row[2],
                'author': row[3],
                'publisher_name': row[4],
                'type_name': row[5],
                'order_quantity': row[6],
                'arrived_quantity': row[7],
                'issued_quantity': row[8],
                'current_quantity': row[9]
            }
        return None
    
    def get_statistics_by_date_range(self, start_date, end_date):
        """按日期范围统计"""
        result = db.session.execute(
            text(f"CALL sp_statistics_by_date_range('{start_date}', '{end_date}')")
        )
        rows = result.fetchall()
        
        data = []
        for row in rows:
            data.append({
                'month': row[0],
                'order_quantity': row[1],
                'arrived_quantity': row[2],
                'issued_quantity': row[3]
            })
        
        return data
    
    def get_inventory_warnings(self):
        """获取库存预警（使用视图v_inventory_warning）"""
        result = db.session.execute(text("""
            SELECT 
                textbook_id,
                isbn,
                textbook_name,
                publisher_name,
                type_name,
                current_quantity,
                min_quantity,
                max_quantity,
                warning_status
            FROM v_inventory_warning
            ORDER BY warning_level ASC, gap_quantity DESC
        """))
        rows = result.fetchall()
        
        data = []
        for row in rows:
            data.append({
                'textbook_id': row[0],
                'isbn': row[1],
                'textbook_name': row[2],
                'publisher_name': row[3],
                'type_name': row[4],
                'current_quantity': row[5],
                'min_quantity': row[6],
                'max_quantity': row[7],
                'status': row[8]  # warning_status 映射为 status，保持接口一致
            })
        
        return data
    
    def get_dashboard_data(self):
        """获取仪表盘数据"""
        # 获取各种统计数据
        from app.models.textbook import Textbook
        from app.models.purchase_order import PurchaseOrder
        
        textbook_count = Textbook.query.filter_by(status=1).count()
        pending_orders = PurchaseOrder.query.filter(
            PurchaseOrder.order_status.in_(['待审核', '已审核', '已订购'])
        ).count()
        
        # 库存总价值
        inventory_value = self.inventory_dao.get_total_value()
        
        # 库存预警数量
        warnings = self.inventory_dao.get_warnings()
        warning_count = len(warnings)
        
        return {
            'textbook_count': textbook_count,
            'pending_orders': pending_orders,
            'pending_requisitions': 0,  # 已移除领用功能，保留字段以兼容前端
            'inventory_value': inventory_value,
            'warning_count': warning_count
        }

