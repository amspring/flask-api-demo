# -*- coding: utf-8 -*-
# File     : cmd.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 18:06
# Remarks  :
from app import create_app
from app.tasks import make_celery

celery = make_celery(__name__)
app = create_app(celery=celery)

if __name__ == '__main__':
    from app.conf import settings

    app.run(host=settings.app.host, port=settings.app.port, use_debugger=False, use_reloader=True)
