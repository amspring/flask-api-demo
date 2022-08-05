# -*- coding: utf-8 -*-
# File     : initialize.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-03 14:16
# Remarks  :  初始化数据库数据脚本

import click
from flask import Flask
from sqlalchemy import event

from .conf import settings
from .logger import logger
from .models import db, Role
from .repositories.user import UserRepository


def register_initialize(app: Flask):
    @app.cli.command()
    @click.option('--action', required=False, type=click.Choice(['create', 'reset', 'drop']))
    def data(action):
        """
        初始化数据: flask data --action  reset
        :param action:
        :return:
        """

        if action == "create":
            db.create_all()
        elif action == "reset":
            db.drop_all()
            db.create_all()
        elif action == "drop":
            db.drop_all()
        else:
            pass

        click.echo(f"--Initialize {action} data success--")

    @app.cli.command()
    @click.option("--username", required=True, type=str)
    @click.option("--mobile", required=True, type=str)
    @click.option("--email", required=True, type=str)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def admin(username, mobile, password, email):
        """
        初始化数据: flask admin --username "老六" --mobile "13599998888" --email "123@dd.com"
        :param username:
        :param mobile:
        :param password:
        :param email
        :return:
        """
        UserRepository.rep_add({
            "username": username,
            "mobile": mobile,
            "password": password,
            "email": email
        })
        click.echo('--Initialize admin success--')


@event.listens_for(Role.__table__, 'after_create')
def initialize_role(*args, **kwargs):
    """
    建表初始化角色表
    :param args:
    :param kwargs:
    :return:
    """
    res = db.session.execute(
        Role.__table__.insert(),
        [role for role in settings.roles]
    )
    db.session.commit()
    logger.info(f"--Initialize role success--")

# @event.listens_for(User.__table__, 'after_create')
# def initialize_admin(*args, **kwargs):
#     """
#     初始化管理员
#     :param args:
#     :param kwargs:
#     :return:
#     """
#     db.session.bulk_save_objects(
#         [
#             User(username=user.get("username"), passwd=user.get("password"), mobile=user.get("mobile"))
#             for user in settings.admins
#         ]
#     )
#     db.session.commit()
