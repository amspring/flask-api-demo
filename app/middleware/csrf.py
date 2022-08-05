# -*- coding: utf-8 -*-
# File     : csrf.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 09:41
# Remarks  :
from flask_wtf.csrf import CSRFProtect
from flask import Flask

csrf = CSRFProtect()


def register_csrf(app: Flask):
    """
    跨站请求伪造
    :param app:
    :return:
    """
    csrf.init_app(app)
