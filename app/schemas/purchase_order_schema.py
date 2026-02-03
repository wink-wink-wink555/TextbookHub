"""
订购Schema
"""
from marshmallow import Schema, fields, validates, ValidationError


class PurchaseOrderSchema(Schema):
    """订购数据验证Schema"""
    
    order_id = fields.Int(dump_only=True)
    order_no = fields.Str(dump_only=True)
    textbook_id = fields.Int(required=True)
    order_quantity = fields.Int(required=True)
    order_date = fields.Date(required=True)
    expected_date = fields.Date(allow_none=True)
    order_person = fields.Str(allow_none=True)
    order_status = fields.Str(dump_only=True)
    arrived_quantity = fields.Int(dump_only=True)
    remarks = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('order_quantity')
    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError('订购数量必须大于0')


class PurchaseOrderUpdateSchema(Schema):
    """订购更新Schema"""
    
    order_quantity = fields.Int()
    expected_date = fields.Date(allow_none=True)
    order_person = fields.Str(allow_none=True)
    remarks = fields.Str(allow_none=True)

