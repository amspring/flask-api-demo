# -*- coding: utf-8 -*-
# File     : exception.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 10:23
# Remarks  :

from flask_restful import Api as _Api
from werkzeug.exceptions import HTTPException


class Api(_Api):

    def error_router(self, original_handler, e):
        """ Override original error_router to only handle HTTPExceptions. """
        if self._has_fr_route() and isinstance(e, HTTPException):
            try:
                return self.handle_error(e)
            except Exception:
                pass  # Fall through to original handler
        return original_handler(e)
