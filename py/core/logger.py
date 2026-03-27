"""
日志拦截器模块
提供统一的请求日志记录和错误处理
"""

import logging
import traceback
from datetime import datetime
from typing import Callable
from flask import request, g, Response
from functools import wraps


# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


class RequestLogger:
    """请求日志拦截器"""
    
    @staticmethod
    def before_request():
        """请求前记录"""
        g.start_time = datetime.now()
        g.request_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
        
        logger.info(
            f"[{g.request_id}] >>> 请求开始 "
            f"{request.method} {request.path} "
            f"IP: {request.remote_addr}"
        )
        
        # 记录请求体（排除敏感字段）
        if request.is_json:
            body = request.get_json(silent=True) or {}
            safe_body = {k: '***' if k in ['password', 'confirm_password'] else v 
                        for k, v in body.items()}
            logger.info(f"[{g.request_id}] 请求体: {safe_body}")
    
    @staticmethod
    def after_request(response: Response) -> Response:
        """请求后记录"""
        # 计算请求耗时
        duration = None
        if hasattr(g, 'start_time'):
            duration = (datetime.now() - g.start_time).total_seconds() * 1000
        
        request_id = getattr(g, 'request_id', 'unknown')
        
        # 记录响应信息
        log_level = logging.ERROR if response.status_code >= 400 else logging.INFO
        logger.log(
            log_level,
            f"[{request_id}] <<< 响应结束 "
            f"状态码: {response.status_code} "
            f"耗时: {duration:.2f}ms"
        )
        
        return response
    
    @staticmethod
    def teardown_request(exception=None):
        """请求结束时处理异常"""
        if exception:
            request_id = getattr(g, 'request_id', 'unknown')
            logger.error(
                f"[{request_id}] !!! 请求异常: {str(exception)}\n"
                f"{traceback.format_exc()}"
            )


def log_errors(func: Callable) -> Callable:
    """装饰器：捕获并记录函数中的错误"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            request_id = getattr(g, 'request_id', 'unknown')
            error_detail = traceback.format_exc()
            logger.error(
                f"[{request_id}] 函数执行错误 [{func.__name__}]: {str(e)}\n"
                f"{error_detail}"
            )
            raise
    return wrapper


def init_logger(app):
    """
    初始化日志拦截器
    
    Args:
        app: Flask 应用实例
    """
    # 请求前钩子
    app.before_request(RequestLogger.before_request)
    
    # 请求后钩子
    app.after_request(RequestLogger.after_request)
    
    # 请求结束钩子（处理未捕获的异常）
    app.teardown_request(RequestLogger.teardown_request)
    
    # 全局异常处理
    @app.errorhandler(Exception)
    def handle_exception(e):
        """捕获所有未处理的异常"""
        request_id = getattr(g, 'request_id', 'unknown')
        error_detail = traceback.format_exc()
        
        logger.error(
            f"[{request_id}] 全局异常捕获: {str(e)}\n"
            f"{error_detail}"
        )
        
        # 返回统一的错误响应
        return {
            "success": False,
            "message": f"服务器内部错误: {str(e)}",
            "request_id": request_id
        }, 500
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        """处理 400 错误"""
        request_id = getattr(g, 'request_id', 'unknown')
        logger.warning(f"[{request_id}] 400 错误: {str(e)}")
        return {
            "success": False,
            "message": "请求参数错误",
            "request_id": request_id
        }, 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """处理 404 错误"""
        request_id = getattr(g, 'request_id', 'unknown')
        logger.warning(f"[{request_id}] 404 错误: {request.path}")
        return {
            "success": False,
            "message": f"请求的资源不存在: {request.path}",
            "request_id": request_id
        }, 404
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        """处理 500 错误"""
        request_id = getattr(g, 'request_id', 'unknown')
        logger.error(f"[{request_id}] 500 错误: {str(e)}")
        return {
            "success": False,
            "message": "服务器内部错误",
            "request_id": request_id
        }, 500
    
    logger.info("日志拦截器初始化完成")


# 导出
__all__ = ['init_logger', 'log_errors', 'logger', 'RequestLogger']
