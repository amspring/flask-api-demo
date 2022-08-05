# -*- coding: utf-8 -*-
# File     : containers.py.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 15:55
# Remarks  :
"""Containers module."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[".blueprints"])
    config = providers.Configuration()
