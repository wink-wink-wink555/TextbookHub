"""
教材Schema
"""
from marshmallow import Schema, fields, validates
from app.utils.validators import validate_isbn, validate_positive_number
from datetime import date


class TextbookSchema(Schema):
    """教材数据验证Schema"""
    
    textbook_id = fields.Int(dump_only=True)
    isbn = fields.Str(required=True)
    textbook_name = fields.Str(required=True, validate=lambda x: len(x) <= 200)
    author = fields.Str(allow_none=True)
    publisher_id = fields.Int(required=True)
    type_id = fields.Int(required=True)
    edition = fields.Str(allow_none=True)
    publication_date = fields.Date(allow_none=True)
    price = fields.Decimal(required=True, as_string=True)
    description = fields.Str(allow_none=True)
    status = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('isbn')
    def validate_isbn_field(self, value):
        validate_isbn(value)
    
    @validates('price')
    def validate_price_field(self, value):
        if value <= 0:
            raise ValidationError('价格必须大于0')


class TextbookUpdateSchema(Schema):
    """教材更新Schema"""
    
    textbook_name = fields.Str()
    author = fields.Str(allow_none=True)
    publisher_id = fields.Int()
    type_id = fields.Int()
    edition = fields.Str(allow_none=True)
    publication_date = fields.Date(allow_none=True)
    price = fields.Decimal(as_string=True)
    description = fields.Str(allow_none=True)

