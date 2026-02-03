"""
统计API
"""
from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1 import api_v1
from app.services.statistics_service import StatisticsService
from app.utils.response import success_response, error_response
from app.utils.decorators import teacher_required, warehouse_required


statistics_service = StatisticsService()


@api_v1.route('/statistics/by-type', methods=['GET'])
@jwt_required()
def get_statistics_by_type():
    """按类型统计（所有登录用户）"""
    try:
        result = statistics_service.get_statistics_by_type()
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/statistics/by-publisher', methods=['GET'])
@jwt_required()
def get_statistics_by_publisher():
    """按出版社统计（所有登录用户）"""
    try:
        result = statistics_service.get_statistics_by_publisher()
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/statistics/by-textbook/<int:textbook_id>', methods=['GET'])
@jwt_required()
def get_statistics_by_textbook(textbook_id):
    """按教材统计（所有登录用户）"""
    try:
        result = statistics_service.get_statistics_by_textbook(textbook_id)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/statistics/by-date', methods=['GET'])
@jwt_required()
def get_statistics_by_date():
    """按日期范围统计（所有登录用户）"""
    try:
        start_date = request.args.get('start_date', required=True)
        end_date = request.args.get('end_date', required=True)
        
        result = statistics_service.get_statistics_by_date_range(start_date, end_date)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/statistics/inventory-warnings', methods=['GET'])
@jwt_required()
@warehouse_required
def get_inventory_warnings():
    """获取库存预警（仅管理员和仓库管理员）"""
    try:
        result = statistics_service.get_inventory_warnings()
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/statistics/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """获取仪表盘数据（所有登录用户）"""
    try:
        result = statistics_service.get_dashboard_data()
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))

