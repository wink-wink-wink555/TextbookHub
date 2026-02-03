"""
全局错误处理器
"""
from flask import current_app
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended.exceptions import JWTExtendedException
from app.utils.exceptions import (
    BusinessException,
    AuthException,
    PermissionException,
    NotFoundException,
    DatabaseException
)
from app.utils.response import error_response


def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """处理数据验证错误"""
        current_app.logger.warning(f'数据验证错误: {e.messages}')
        return error_response(
            message='数据验证失败',
            code=400,
            errors=e.messages
        )
    
    @app.errorhandler(AuthException)
    def handle_auth_error(e):
        """处理认证错误"""
        current_app.logger.warning(f'认证错误: {e.message}')
        return error_response(message=e.message, code=e.code)
    
    @app.errorhandler(PermissionException)
    def handle_permission_error(e):
        """处理权限错误"""
        current_app.logger.warning(f'权限错误: {e.message}')
        return error_response(message=e.message, code=e.code)
    
    @app.errorhandler(NotFoundException)
    def handle_not_found_error(e):
        """处理资源不存在错误"""
        current_app.logger.warning(f'资源不存在: {e.message}')
        return error_response(message=e.message, code=e.code)
    
    @app.errorhandler(DatabaseException)
    def handle_database_error(e):
        """处理数据库错误"""
        current_app.logger.error(f'数据库错误: {e.message}')
        return error_response(message=e.message, code=e.code)
    
    @app.errorhandler(BusinessException)
    def handle_business_error(e):
        """处理业务异常"""
        current_app.logger.warning(f'业务异常: {e.message}')
        return error_response(message=e.message, code=e.code)
    
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(e):
        """处理SQLAlchemy错误"""
        current_app.logger.error(f'数据库错误: {str(e)}')
        return error_response(
            message='数据库操作失败',
            code=500
        )
    
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_error(e):
        """处理JWT错误"""
        current_app.logger.warning(f'JWT错误: {str(e)}')
        return error_response(
            message='认证失败，请重新登录',
            code=401
        )
    
    @app.errorhandler(404)
    def handle_404_error(e):
        """处理404错误"""
        return error_response(message='请求的资源不存在', code=404)
    
    @app.errorhandler(405)
    def handle_405_error(e):
        """处理405错误"""
        return error_response(message='不支持的请求方法', code=405)
    
    @app.errorhandler(500)
    def handle_500_error(e):
        """处理500错误"""
        current_app.logger.error(f'服务器错误: {str(e)}')
        return error_response(message='服务器内部错误', code=500)
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        """处理未预期的错误"""
        current_app.logger.error(f'未预期的错误: {str(e)}', exc_info=True)
        return error_response(
            message='服务器发生未知错误',
            code=500
        )

