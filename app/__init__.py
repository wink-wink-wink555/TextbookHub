"""
Flask应用工厂
"""
from flask import Flask, render_template
from flask_cors import CORS
from config import config
from app.extensions import db, jwt, migrate
from app.middleware.error_handler import register_error_handlers
from app.utils.response import success_response
import logging
import os


def create_app(config_name='default'):
    """
    应用工厂函数
    :param config_name: 配置名称
    :return: Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    init_extensions(app)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 配置CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # 配置日志
    setup_logging(app)
    
    # 前端路由
    @app.route('/')
    def index():
        return app.send_static_file('index.html') if os.path.exists(os.path.join(app.root_path, 'static', 'index.html')) else render_template('login.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/textbooks')
    def textbooks_page():
        return render_template('textbooks.html')
    
    @app.route('/publishers')
    def publishers_page():
        return render_template('publishers.html')
    
    @app.route('/orders')
    def orders_page():
        return render_template('orders.html')
    
    @app.route('/statistics')
    def statistics_page():
        return render_template('statistics.html')
    
    # API健康检查
    @app.route('/api/health')
    def health():
        return success_response(message='服务运行正常')
    
    return app


def init_extensions(app):
    """初始化Flask扩展"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """注册蓝图"""
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')


def setup_logging(app):
    """配置日志"""
    if not app.debug:
        # 创建日志目录
        log_dir = app.config.get('LOG_DIR', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 配置文件处理器
        file_handler = logging.FileHandler(
            os.path.join(log_dir, 'app.log'),
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        
        # 配置错误日志处理器
        error_handler = logging.FileHandler(
            os.path.join(log_dir, 'error.log'),
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        
        app.logger.addHandler(file_handler)
        app.logger.addHandler(error_handler)
        app.logger.setLevel(logging.INFO)

