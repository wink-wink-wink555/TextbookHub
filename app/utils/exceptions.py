"""
自定义异常类
"""


class BusinessException(Exception):
    """业务异常基类"""
    
    def __init__(self, message='业务处理失败', code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationException(BusinessException):
    """数据验证异常"""
    
    def __init__(self, message='数据验证失败', errors=None):
        super().__init__(message, 400)
        self.errors = errors


class AuthException(BusinessException):
    """认证异常"""
    
    def __init__(self, message='认证失败', code=401):
        super().__init__(message, code)


class PermissionException(BusinessException):
    """权限异常"""
    
    def __init__(self, message='权限不足', code=403):
        super().__init__(message, code)


class NotFoundException(BusinessException):
    """资源不存在异常"""
    
    def __init__(self, message='资源不存在', code=404):
        super().__init__(message, code)


class DatabaseException(BusinessException):
    """数据库异常"""
    
    def __init__(self, message='数据库操作失败', code=500):
        super().__init__(message, code)

