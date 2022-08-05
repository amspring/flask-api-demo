# -*- coding: utf-8 -*-
# File     : db.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 16:08
# Remarks  :

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(use_native_unicode='utf8mb4')
migrate = Migrate()


def register_db(app: Flask):
    """
    注册数据库
    :param app:
    :return:
    """
    db.init_app(app)
    migrate.init_app(app, db)
