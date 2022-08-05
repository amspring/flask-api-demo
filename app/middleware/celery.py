# -*- coding: utf-8 -*-
# File     : celery.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 15:43
# Remarks  :
from flask import Flask


def register_celery(celery, app: Flask):
    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
