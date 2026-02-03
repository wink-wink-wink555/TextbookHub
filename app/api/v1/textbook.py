"""
教材API
"""
from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1 import api_v1
from app.services.textbook_service import TextbookService
from app.schemas.textbook_schema import TextbookSchema, TextbookUpdateSchema
from app.utils.response import success_response, error_response, paginated_response
from app.utils.helpers import get_pagination_params
from app.utils.decorators import admin_required
from marshmallow import ValidationError


textbook_service = TextbookService()


@api_v1.route('/textbooks', methods=['GET'])
@jwt_required()
def get_textbooks():
    """获取教材列表（所有登录用户可查看）"""
    try:
        page, per_page = get_pagination_params()
        keyword = request.args.get('keyword')
        publisher_id = request.args.get('publisher_id', type=int)
        type_id = request.args.get('type_id', type=int)
        
        items, total = textbook_service.get_textbook_list(
            page=page,
            per_page=per_page,
            keyword=keyword,
            publisher_id=publisher_id,
            type_id=type_id
        )
        
        return paginated_response(items, total, page, per_page)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/textbooks/<int:textbook_id>', methods=['GET'])
@jwt_required()
def get_textbook(textbook_id):
    """获取教材详情（所有登录用户可查看）"""
    try:
        result = textbook_service.get_textbook_detail(textbook_id)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/textbooks', methods=['POST'])
@jwt_required()
@admin_required
def create_textbook():
    """创建教材（仅管理员）"""
    try:
        schema = TextbookSchema()
        data = schema.load(request.get_json())
        
        result = textbook_service.create_textbook(data)
        return success_response(data=result, message='创建成功', code=201)
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/textbooks/<int:textbook_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_textbook(textbook_id):
    """更新教材（仅管理员）"""
    try:
        schema = TextbookUpdateSchema()
        data = schema.load(request.get_json())
        
        result = textbook_service.update_textbook(textbook_id, data)
        return success_response(data=result, message='更新成功')
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/textbooks/<int:textbook_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_textbook(textbook_id):
    """删除教材（仅管理员）"""
    try:
        textbook_service.delete_textbook(textbook_id)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e))

