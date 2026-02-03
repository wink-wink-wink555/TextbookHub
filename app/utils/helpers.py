"""
辅助函数
"""
from datetime import datetime
import bcrypt


def hash_password(password):
    """
    加密密码
    :param password: 明文密码
    :return: 加密后的密码
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    """
    验证密码
    :param password: 明文密码
    :param hashed_password: 加密后的密码
    :return: 是否匹配
    """
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def format_datetime(dt, fmt='%Y-%m-%d %H:%M:%S'):
    """
    格式化日期时间
    :param dt: datetime对象
    :param fmt: 格式字符串
    :return: 格式化后的字符串
    """
    if dt:
        return dt.strftime(fmt)
    return None


def parse_datetime(date_string, fmt='%Y-%m-%d %H:%M:%S'):
    """
    解析日期时间字符串
    :param date_string: 日期时间字符串
    :param fmt: 格式字符串
    :return: datetime对象
    """
    if date_string:
        return datetime.strptime(date_string, fmt)
    return None


def get_pagination_params(default_page=1, default_per_page=20, max_per_page=100):
    """
    从请求中获取分页参数
    :param default_page: 默认页码
    :param default_per_page: 默认每页数量
    :param max_per_page: 最大每页数量
    :return: (page, per_page)
    """
    from flask import request
    
    page = request.args.get('page', default_page, type=int)
    per_page = request.args.get('per_page', default_per_page, type=int)
    
    # 确保页码最小为1
    page = max(1, page)
    
    # 限制每页数量
    per_page = min(max_per_page, max(1, per_page))
    
    return page, per_page

