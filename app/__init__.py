# -*- coding: utf-8 -*-
# File     : __init__.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 15:56
# Remarks  :
from flask import Flask

from . import config
from .logger import logger
from .conf import settings
from .containers import Container
from .blueprints import api
from .initialize import register_initialize
from .middleware import register_db, register_cor, register_csrf, register_redis, register_celery


def create_app(**kwargs) -> Flask:
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config)
    # 注册依赖
    container = Container()
    app.container = container
    # 注册蓝图
    app.register_blueprint(api, url_prefix=settings.app.prefix)
    # 注册redis
    register_redis(app)
    # 注册DB
    register_db(app)
    # 注册跨域
    register_cor(app)
    # 跨站请求伪造
    register_csrf(app)
    # 初始化数据库脚本
    register_initialize(app)

    # 注册异步任务
    try:
        register_celery(celery=kwargs.get('celery'), app=app)
    except Exception as e:
        logger.error(f"register celery cause error: {str(e)}")

    return app
