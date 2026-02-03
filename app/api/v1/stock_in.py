"""
入库API
"""
from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1 import api_v1
from app.services.stock_in_service import StockInService
from app.schemas.stock_in_schema import StockInSchema, StockInUpdateSchema
from app.utils.response import success_response, error_response, paginated_response
from app.utils.helpers import get_pagination_params
from app.utils.decorators import warehouse_required, admin_required
from marshmallow import ValidationError


stock_in_service = StockInService()


@api_v1.route('/stock-ins', methods=['GET'])
@jwt_required()
@warehouse_required
def get_stock_ins():
    """获取入库列表（仅管理员和仓库管理员）"""
    try:
        page, per_page = get_pagination_params()
        keyword = request.args.get('keyword')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        items, total = stock_in_service.get_stock_in_list(
            page=page,
            per_page=per_page,
            keyword=keyword,
            start_date=start_date,
            end_date=end_date
        )
        
        return paginated_response(items, total, page, per_page)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/stock-ins/<int:stock_in_id>', methods=['GET'])
@jwt_required()
@warehouse_required
def get_stock_in(stock_in_id):
    """获取入库详情（仅管理员和仓库管理员）"""
    try:
        result = stock_in_service.get_stock_in_detail(stock_in_id)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/stock-ins', methods=['POST'])
@jwt_required()
@warehouse_required
def create_stock_in():
    """创建入库单（仅管理员和仓库管理员）"""
    try:
        schema = StockInSchema()
        data = schema.load(request.get_json())
        
        result = stock_in_service.create_stock_in(data)
        return success_response(data=result, message='入库成功，库存已自动更新', code=201)
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/stock-ins/<int:stock_in_id>', methods=['PUT'])
@jwt_required()
@warehouse_required
def update_stock_in(stock_in_id):
    """更新入库单（仅管理员和仓库管理员）"""
    try:
        schema = StockInUpdateSchema()
        data = schema.load(request.get_json())
        
        result = stock_in_service.update_stock_in(stock_in_id, data)
        return success_response(data=result, message='更新成功')
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/stock-ins/<int:stock_in_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_stock_in(stock_in_id):
    """删除入库单（仅管理员，会自动回退库存）"""
    try:
        result = stock_in_service.delete_stock_in(stock_in_id)
        return success_response(message='删除成功，库存已自动回退')
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/stock-ins/direct', methods=['POST'])
@jwt_required()
@warehouse_required
def direct_stock_in():
    """
    直接入库（不依赖现有订单）
    - 自动创建一个"直接采购"订单
    - 然后执行入库操作
    - 仅管理员和仓库管理员可操作
    """
    try:
        from flask_jwt_extended import get_jwt
        from app.services.purchase_service import PurchaseService
        from datetime import date
        
        current_user = get_jwt()
        username = current_user.get('username')
        
        data = request.get_json()
        textbook_id = data.get('textbook_id')
        quantity = data.get('quantity')
        remarks = data.get('remarks', '直接入库')
        
        if not textbook_id or not quantity:
            return error_response(message='教材ID和入库数量不能为空', code=400)
        
        if quantity <= 0:
            return error_response(message='入库数量必须大于0', code=400)
        
        # 1. 自动创建一个"直接采购"订单（状态直接设为已审核）
        purchase_service = PurchaseService()
        order_data = {
            'textbook_id': textbook_id,
            'order_quantity': quantity,
            'order_date': date.today().strftime('%Y-%m-%d'),
            'order_person': username,
            'order_status': '已审核',  # 直接设为已审核
            'remarks': f'直接入库 - {remarks}'
        }
        order_result = purchase_service.create_order(order_data)
        order_id = order_result.get('order_id')
        
        # 2. 执行入库操作
        stock_in_data = {
            'order_id': order_id,
            'textbook_id': textbook_id,
            'stock_in_quantity': quantity,
            'stock_in_date': date.today().strftime('%Y-%m-%d'),
            'warehouse_person': username,
            'quality_status': data.get('quality_status', '合格'),
            'actual_quantity': quantity,
            'remarks': remarks
        }
        result = stock_in_service.create_stock_in(stock_in_data)
        
        return success_response(data=result, message='直接入库成功，库存已更新', code=201)
    except Exception as e:
        return error_response(message=str(e))
