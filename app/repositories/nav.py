# -*- coding: utf-8 -*-
# File     : nav.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 09:37
# Remarks  :
from flask_restful import abort

from ..models import Nav
from ..middleware.database import db


class NavRepository(object):

    def __init__(self):
        pass

    @staticmethod
    def rep_get_all(page, per_page, args=None) -> (list, int):
        """
        :param page:
        :param per_page:
        :param args:
        :return:
        """
        if args is None:
            args = {}

        f = Nav.query.filter(**args)
        pagination = f.paginate(page, per_page, error_out=False)

        return pagination.items, pagination.total

    @staticmethod
    def rep_get(args) -> Nav:
        """
        :param args:
        :return:
        """
        return Nav.query.filter_by(**args).first()

    @staticmethod
    def rep_add(args) -> dict:
        """
        :param args:
        :return:
        """
        try:
            item = Nav(**args)
            db.session.add(item)
            db.session.commit()
            return {"id": item.id}
        except Exception as e:
            abort(http_status_code=400, messages=repr(e.orig))

    @staticmethod
    def rep_bulk_add(args) -> bool:
        """
        批量插入
        :param args:
        :return:
        """
        try:
            res = db.session.execute(
                Nav.__table__.insert(),
                [nav for nav in args]
            )
            db.session.commit()
            return True
        except Exception as e:
            abort(http_status_code=400, messages=repr(e.orig))

    @staticmethod
    def rep_update(_id, args) -> int:
        """
        :param _id:
        :param args:
        :return:
        """
        try:
            total = Nav.query.filter_by(id=_id).update(args)
            db.session.commit()
            return total
        except Exception as e:
            abort(http_status_code=400, messages=repr(e.orig))

    @staticmethod
    def rep_delete(_id) -> int:
        """
        :param _id:
        :return:
        """
        total = Nav.query.filter_by(id=_id).delete(synchronize_session=False)
        db.session.commit()
        return total
