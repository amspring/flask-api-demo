# -*- coding: utf-8 -*-
# File     : __init__.py.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 15:42
# Remarks  :
from .cor import register_cor
from .database import register_db
from .redis import register_redis
from .csrf import register_csrf
from .celery import register_celery

__all__ = ["register_cor", "register_db", "register_redis", "register_csrf", "register_celery"]
