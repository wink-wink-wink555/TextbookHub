"""
出版社Schema
"""
from marshmallow import Schema, fields, validates, ValidationError
from app.utils.validators import validate_phone, validate_email


class PublisherSchema(Schema):
    """出版社数据验证Schema"""
    
    publisher_id = fields.Int(dump_only=True)
    publisher_name = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    contact_person = fields.Str(allow_none=True)
    contact_phone = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    email = fields.Str(allow_none=True)
    status = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('contact_phone')
    def validate_phone_field(self, value):
        if value:
            validate_phone(value)
    
    @validates('email')
    def validate_email_field(self, value):
        if value:
            validate_email(value)


class PublisherUpdateSchema(Schema):
    """出版社更新Schema"""
    
    publisher_name = fields.Str()
    contact_person = fields.Str(allow_none=True)
    contact_phone = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    email = fields.Str(allow_none=True)

