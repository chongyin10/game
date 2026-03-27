"""
Flask API 服务入口
提供 RESTful API 接口供前端调用

启动服务:
    python app.py
    
或者使用 Flask CLI:
    flask --app app run
"""

from flask import Flask
from flask_cors import CORS
from routes.userinfo_routes import userinfo_bp
from routes.auth_routes import auth_bp
from core.logger import init_logger


def create_app() -> Flask:
    """创建 Flask 应用实例"""
    app = Flask(__name__)
    
    # 初始化日志拦截器
    init_logger(app)
    
    # 启用 CORS，允许前端跨域访问并携带 cookie
    CORS(app, origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3333",
        "http://127.0.0.1:3333",
    ], supports_credentials=True)
    
    # 注册蓝图
    app.register_blueprint(userinfo_bp, url_prefix='/api/userinfo')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    @app.route('/')
    def index():
        return {
            "message": "API 服务运行中",
            "docs": {
                "userinfo": "/api/userinfo",
                "auth": "/api/auth"
            }
        }
    
    @app.route('/health')
    def health():
        return {"status": "ok"}
    
    return app


if __name__ == "__main__":
    app = create_app()
    print("=" * 50)
    print("Flask API 服务启动")
    print("=" * 50)
    print("API 地址: http://127.0.0.1:5002")
    print("UserInfo API: http://127.0.0.1:5002/api/userinfo")
    print("Auth API: http://127.0.0.1:5002/api/auth")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5002)
