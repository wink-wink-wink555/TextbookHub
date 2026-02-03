"""
入库DAO
"""
from app.dao.base_dao import BaseDAO
from app.models.stock_in import StockIn
from app.extensions import db


class StockInDAO(BaseDAO):
    """入库数据访问对象"""
    
    def __init__(self):
        super().__init__(StockIn)
    
    def get_by_stock_in_no(self, stock_in_no):
        """根据入库单号查询"""
        return self.model.query.filter_by(stock_in_no=stock_in_no).first()
    
    def get_by_order(self, order_id):
        """获取指定订单的所有入库记录"""
        return self.model.query.filter_by(order_id=order_id).order_by(
            self.model.stock_in_date.desc()
        ).all()
    
    def get_by_textbook(self, textbook_id):
        """获取指定教材的所有入库记录"""
        return self.model.query.filter_by(textbook_id=textbook_id).order_by(
            self.model.stock_in_date.desc()
        ).all()
    
    def search(self, keyword=None, start_date=None, end_date=None, 
               page=1, per_page=20):
        """
        多条件搜索
        :param keyword: 搜索关键字
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param page: 页码
        :param per_page: 每页数量
        :return: (items, total)
        """
        query = self.model.query
        
        if keyword:
            query = query.filter(
                db.or_(
                    self.model.stock_in_no.like(f'%{keyword}%'),
                    self.model.warehouse_person.like(f'%{keyword}%')
                )
            )
        
        if start_date:
            query = query.filter(self.model.stock_in_date >= start_date)
        
        if end_date:
            query = query.filter(self.model.stock_in_date <= end_date)
        
        total = query.count()
        items = query.order_by(
            self.model.stock_in_date.desc()
        ).limit(per_page).offset((page - 1) * per_page).all()
        return items, total

