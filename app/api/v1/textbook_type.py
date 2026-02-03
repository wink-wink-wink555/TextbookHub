"""
教材类型API
"""
from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1 import api_v1
from app.dao.textbook_type_dao import TextbookTypeDAO
from app.utils.response import success_response, error_response
from app.utils.decorators import admin_required
from marshmallow import Schema, fields, ValidationError


textbook_type_dao = TextbookTypeDAO()


class TextbookTypeSchema(Schema):
    """教材类型Schema"""
    type_name = fields.String(required=True, error_messages={'required': '类型名称不能为空'})
    type_code = fields.String(required=True, error_messages={'required': '类型编码不能为空'})
    description = fields.String(allow_none=True)
    parent_id = fields.Integer(allow_none=True)


class TextbookTypeUpdateSchema(Schema):
    """教材类型更新Schema"""
    type_name = fields.String()
    type_code = fields.String()
    description = fields.String(allow_none=True)
    parent_id = fields.Integer(allow_none=True)


@api_v1.route('/textbook-types', methods=['GET'])
@jwt_required()
def get_textbook_types():
    """获取教材类型列表（所有登录用户可查看）"""
    try:
        types = textbook_type_dao.get_active_types()
        result = [t.to_dict() for t in types]
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/textbook-types/tree', methods=['GET'])
@jwt_required()
def get_textbook_types_tree():
    """获取教材类型树形结构（所有登录用户可查看）"""
    try:
        tree = textbook_type_dao.get_tree()
        return success_response(data=tree)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/textbook-types/<int:type_id>', methods=['GET'])
@jwt_required()
def get_textbook_type(type_id):
    """获取教材类型详情（所有登录用户可查看）"""
    try:
        textbook_type = textbook_type_dao.get_by_id(type_id)
        result = textbook_type.to_dict(include_children=True)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/textbook-types', methods=['POST'])
@jwt_required()
@admin_required
def create_textbook_type():
    """创建教材类型（仅管理员）"""
    try:
        schema = TextbookTypeSchema()
        data = schema.load(request.get_json())
        
        textbook_type = textbook_type_dao.create(data)
        result = textbook_type.to_dict()
        
        return success_response(data=result, message='创建成功', code=201)
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/textbook-types/<int:type_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_textbook_type(type_id):
    """更新教材类型（仅管理员）"""
    try:
        schema = TextbookTypeUpdateSchema()
        data = schema.load(request.get_json())
        
        textbook_type = textbook_type_dao.update(type_id, data)
        result = textbook_type.to_dict()
        
        return success_response(data=result, message='更新成功')
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/textbook-types/<int:type_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_textbook_type(type_id):
    """删除教材类型（仅管理员，软删除）"""
    try:
        textbook_type_dao.delete(type_id, soft=True)
        return success_response(message='删除成功')
    except Exception as e:
        return error_response(message=str(e))

