"""
用户Schema
"""
from marshmallow import Schema, fields, validates, ValidationError
from app.utils.validators import validate_phone, validate_email


class UserSchema(Schema):
    """用户数据验证Schema"""
    
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=lambda x: len(x) <= 50)
    password = fields.Str(required=True, load_only=True)
    real_name = fields.Str(allow_none=True)
    role = fields.Str(allow_none=True)
    department = fields.Str(allow_none=True)
    email = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    status = fields.Int(dump_only=True)
    last_login = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('phone')
    def validate_phone_field(self, value):
        if value:
            validate_phone(value)
    
    @validates('email')
    def validate_email_field(self, value):
        if value:
            validate_email(value)


class LoginSchema(Schema):
    """登录Schema"""
    
    username = fields.Str(required=True)
    password = fields.Str(required=True)

