"""
统一响应格式
"""
from flask import jsonify
import time


def success_response(data=None, message='success', code=200):
    """
    成功响应
    :param data: 响应数据
    :param message: 响应消息
    :param code: 状态码
    :return: JSON响应
    """
    response = {
        'code': code,
        'message': message,
        'data': data,
        'timestamp': int(time.time())
    }
    return jsonify(response), code


def error_response(message='error', code=400, errors=None):
    """
    错误响应
    :param message: 错误消息
    :param code: 状态码
    :param errors: 详细错误信息
    :return: JSON响应
    """
    response = {
        'code': code,
        'message': message,
        'timestamp': int(time.time())
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), code


def paginated_response(items, total, page, per_page, message='success'):
    """
    分页响应
    :param items: 数据列表
    :param total: 总数
    :param page: 当前页码
    :param per_page: 每页数量
    :param message: 响应消息
    :return: JSON响应
    """
    import math
    pages = math.ceil(total / per_page) if per_page > 0 else 0
    
    data = {
        'items': items,
        'pagination': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': pages,
            'has_prev': page > 1,
            'has_next': page < pages
        }
    }
    return success_response(data=data, message=message)

