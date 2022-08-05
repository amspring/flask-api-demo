# -*- coding: utf-8 -*-
# File     : cor.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 15:42
# Remarks  :
from flask import Flask
from flask_cors import CORS


def register_cor(app: Flask):
    """
    注册跨域
    :param app:
    :return:
    """
    CORS(app, supports_credentials=True)
