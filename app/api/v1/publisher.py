"""
出版社API
"""
from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1 import api_v1
from app.dao.publisher_dao import PublisherDAO
from app.schemas.publisher_schema import PublisherSchema, PublisherUpdateSchema
from app.utils.response import success_response, error_response, paginated_response
from app.utils.helpers import get_pagination_params
from app.utils.decorators import admin_required
from marshmallow import ValidationError


publisher_dao = PublisherDAO()


@api_v1.route('/publishers', methods=['GET'])
@jwt_required()
def get_publishers():
    """获取出版社列表（所有登录用户可查看）"""
    try:
        page, per_page = get_pagination_params()
        keyword = request.args.get('keyword')
        
        if keyword:
            items, total = publisher_dao.search_by_keyword(keyword, page, per_page)
        else:
            items, total = publisher_dao.paginate(page=page, per_page=per_page, filters={'status': 1})
        
        schema = PublisherSchema(many=True)
        result = schema.dump(items)
        
        return paginated_response(result, total, page, per_page)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/publishers/<int:publisher_id>', methods=['GET'])
@jwt_required()
def get_publisher(publisher_id):
    """获取出版社详情（所有登录用户可查看）"""
    try:
        publisher = publisher_dao.get_by_id(publisher_id)
        schema = PublisherSchema()
        result = schema.dump(publisher)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/publishers', methods=['POST'])
@jwt_required()
@admin_required
def create_publisher():
    """创建出版社（仅管理员）"""
    try:
        schema = PublisherSchema()
        data = schema.load(request.get_json())
        
        publisher = publisher_dao.create(data)
        result = schema.dump(publisher)
        
        return success_response(data=result, message='创建成功', code=201)
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/publishers/<int:publisher_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_publisher(publisher_id):
    """更新出版社（仅管理员）"""
    try:
        schema = PublisherUpdateSchema()
        data = schema.load(request.get_json())
        
        publisher = publisher_dao.update(publisher_id, data)
        result_schema = PublisherSchema()
        result = result_schema.dump(publisher)
        
        return success_response(data=result, message='更新成功')
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/publishers/<int:publisher_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_publisher(publisher_id):
    """删除出版社（仅管理员，软删除）"""
    try:
        publisher_dao.delete(publisher_id, soft=True)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e))

