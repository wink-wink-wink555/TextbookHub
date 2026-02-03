"""
入库Schema
"""
from marshmallow import Schema, fields, validates, ValidationError


class StockInSchema(Schema):
    """入库创建Schema"""
    order_id = fields.Integer(required=True, error_messages={'required': '订单ID不能为空'})
    textbook_id = fields.Integer(required=True, error_messages={'required': '教材ID不能为空'})
    stock_in_quantity = fields.Integer(required=True, error_messages={'required': '入库数量不能为空'})
    stock_in_date = fields.Date(required=True, error_messages={'required': '入库日期不能为空'})
    warehouse_person = fields.String(allow_none=True)
    quality_status = fields.String(allow_none=True, missing='合格')
    actual_quantity = fields.Integer(required=True, error_messages={'required': '实际入库数量不能为空'})
    remarks = fields.String(allow_none=True)
    
    @validates('stock_in_quantity')
    def validate_stock_in_quantity(self, value):
        if value <= 0:
            raise ValidationError('入库数量必须大于0')
    
    @validates('actual_quantity')
    def validate_actual_quantity(self, value):
        if value < 0:
            raise ValidationError('实际入库数量不能为负数')
    
    @validates('quality_status')
    def validate_quality_status(self, value):
        if value and value not in ['合格', '部分合格', '不合格']:
            raise ValidationError('质量状态只能是：合格、部分合格、不合格')


class StockInUpdateSchema(Schema):
    """入库更新Schema"""
    stock_in_quantity = fields.Integer()
    stock_in_date = fields.Date()
    warehouse_person = fields.String(allow_none=True)
    quality_status = fields.String(allow_none=True)
    actual_quantity = fields.Integer()
    remarks = fields.String(allow_none=True)
    
    @validates('stock_in_quantity')
    def validate_stock_in_quantity(self, value):
        if value <= 0:
            raise ValidationError('入库数量必须大于0')
    
    @validates('actual_quantity')
    def validate_actual_quantity(self, value):
        if value < 0:
            raise ValidationError('实际入库数量不能为负数')
    
    @validates('quality_status')
    def validate_quality_status(self, value):
        if value and value not in ['合格', '部分合格', '不合格']:
            raise ValidationError('质量状态只能是：合格、部分合格、不合格')
