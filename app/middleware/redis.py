# -*- coding: utf-8 -*-
# File     : redis.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 17:47
# Remarks  :
"""
flask_caching => pip update by 2022-06-27 for 2.0.0, need flask version =< 2.1.2

#设置一个缓存对象
cache.set(key,value,timeout=None)

#设置多个缓存对象
cache.set_many([(key,value),(key,value),...,(key,value)],timeout=None)

#获取一个缓存对象
cache.get(key)

#获取多个缓存对象
cache.get_many(key1,key2,....)

#删除一个缓存对象
cache.get.delete(key)

#删除多个缓存对象
cache_delete_many(key1,key2,...) #删除多个缓存对象

#删除所有缓存对象
cache.clear()
"""

from flask import Flask
from flask_caching import Cache

cache = Cache()


def register_redis(app: Flask):
    """
    :param app:
    :return:
    """
    cache.init_app(app=app)
