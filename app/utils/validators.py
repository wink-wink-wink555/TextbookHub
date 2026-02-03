"""
自定义验证器
"""
import re
from marshmallow import ValidationError


def validate_isbn(isbn):
    """
    验证ISBN格式：ISBN + 10位数字
    :param isbn: ISBN编号
    :raises ValidationError: 格式不正确
    """
    pattern = r'^ISBN[0-9]{10}$'
    if not re.match(pattern, isbn):
        raise ValidationError('ISBN格式错误，必须是ISBN开头后跟10位数字，例如：ISBN9787040001')


def validate_phone(phone):
    """
    验证电话号码格式
    :param phone: 电话号码
    :raises ValidationError: 格式不正确
    """
    if phone and not re.match(r'^1[3-9]\d{9}$', phone):
        raise ValidationError('手机号码格式不正确')


def validate_email(email):
    """
    验证邮箱格式
    :param email: 邮箱地址
    :raises ValidationError: 格式不正确
    """
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValidationError('邮箱格式不正确')


def validate_positive_number(value):
    """
    验证正数
    :param value: 数值
    :raises ValidationError: 不是正数
    """
    if value is not None and value <= 0:
        raise ValidationError('数值必须大于0')

