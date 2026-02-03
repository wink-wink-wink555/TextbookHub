"""
API v1版本
"""
from flask import Blueprint

# 创建蓝图
api_v1 = Blueprint('api_v1', __name__)

# 导入所有路由
from app.api.v1 import auth, publisher, textbook, purchase_order, statistics, textbook_type, stock_in

__all__ = ['api_v1']

