# -*- coding: utf-8 -*-
# File     : conf.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 17:41
# Remarks  :

import functools
import os
import yaml
import requests


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Config:

    def __init__(self, *args, **kwargs):
        """装载
        Args:
            *args:
            **kwargs:
        """
        self.kwargs = kwargs

    def init_data(self):
        return self.dict_to_object(self.kwargs)

    def dict_to_object(self, args):
        if not isinstance(args, dict):
            return args
        inst = Dict()
        for k, v in args.items():
            inst[k] = self.dict_to_object(v)
        return inst

    @staticmethod
    def config_file():
        """
        file path
        :return:
        """
        config_path = os.path.abspath(os.path.dirname(__name__))
        config_name = os.getenv("CONFIG_NAME", "config.yml")
        return os.path.join(config_path, config_name)

    @staticmethod
    def local():
        """加载本地配置
        Args:
        Returns:
        """
        config_file = Config.config_file()
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding="utf-8") as f:
                config = yaml.safe_load(f.read())
            return Config(**config).init_data()
        return None

    @staticmethod
    @functools.lru_cache()
    def remote():
        """加载远程配置
        Args:
        Returns:
        """
        config_file = Config.config_file()
        if not os.path.exists(config_file):
            r = requests.get(os.getenv("CONFIG_URL"))
            yaml.dump(yaml.safe_load(r.content), open(os.getenv("CONFIG_NAME", "config.yml"), 'w'), allow_unicode=True)
        return Config.local()


# 加载配置
settings = Config.remote()

__all__ = ["settings"]
