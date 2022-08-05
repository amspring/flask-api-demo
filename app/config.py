# -*- coding: utf-8 -*-
# File     : config.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 16:50
# Remarks  : 配置信息
from .conf import settings

# 密钥
SECRET_KEY = settings.auth.SECRET_KEY

# 上传文件配置
UPLOAD_FOLDER = settings.upload.UPLOAD_FOLDER
MAX_CONTENT_LENGTH = settings.upload.MAX_CONTENT_LENGTH * 1024 * 1024
ALLOWED_EXTENSIONS = set(settings.upload.ALLOWED_EXTENSIONS)

# 数据库配置
SQLALCHEMY_DATABASE_URI = settings.db.SQLALCHEMY_DATABASE_URI
# 每次请求结束时自动commit数据库修改
SQLALCHEMY_TRACK_MODIFICATIONS = settings.db.SQLALCHEMY_TRACK_MODIFICATIONS
# 可以用于显式地禁用或者启用查询记录。查询记录 在调试或者测试模式下自动启用。
SQLALCHEMY_RECORD_QUERIES = settings.db.SQLALCHEMY_RECORD_QUERIES
# True，SQLAlchemy将会记录所有发到标准输出(stderr)的语句, 生产环境关掉.
SQLALCHEMY_ECHO = settings.db.SQLALCHEMY_ECHO
# 数据库连接池的大小。默认是数据库引擎的默认值(通常是 5)。
SQLALCHEMY_POOL_SIZE = settings.db.SQLALCHEMY_POOL_SIZE
# 连接池最大的大小
SQLALCHEMY_POOL_MAX_SIZE = settings.db.SQLALCHEMY_POOL_MAX_SIZE
# 控制在连接池达到最大值后可以创建的连接数。当这些额外的连接使用后回收到连接池后将会被断开和抛弃。保证连接池只有设置的大小
SQLALCHEMY_MAX_OVERFLOW = settings.db.SQLALCHEMY_MAX_OVERFLOW
# 指定数据库连接池的超时时间。默认是 10
SQLALCHEMY_POOL_TIMEOUT = settings.db.SQLALCHEMY_POOL_TIMEOUT
# 多久时间回收连接, flask 默认2个小时回收
SQLALCHEMY_POOL_RECYCLE = settings.db.SQLALCHEMY_POOL_RECYCLE

# flask_caching, CACHE_REDIS_URL = "redis://localhost:6379/0"
CACHE_TYPE = 'RedisCache'  # 使用redis作为缓存, RedisCache、RedisSentinelCache、RedisClusterCache
CACHE_KEY_PREFIX = settings.redis.CACHE_KEY_PREFIX  # 设置cache_key的前缀
CACHE_REDIS_HOST = settings.redis.CACHE_REDIS_HOST  # redis地址
CACHE_REDIS_PORT = settings.redis.CACHE_REDIS_PORT  # redis端口
CACHE_REDIS_PASSWORD = settings.redis.CACHE_REDIS_PASSWORD  # redis密码
CACHE_REDIS_DB = settings.redis.CACHE_REDIS_DB  # 使用哪个数据库
CACHE_DEFAULT_TIMEOUT = settings.redis.CACHE_DEFAULT_TIMEOUT  # 默认过期/超时时间，单位为秒

REDIS_DB = settings.redis.REDIS_DB

# 异步任务redis, https://docs.celeryq.dev/en/latest/userguide/configuration.html
CELERY_BROKER_URL = f"redis://:{CACHE_REDIS_PASSWORD}@{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{REDIS_DB}"
RESULT_BACKEND = f"redis://:{CACHE_REDIS_PASSWORD}@{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{REDIS_DB}"
# 时区
TIMEZONE = 'Asia/Shanghai'
