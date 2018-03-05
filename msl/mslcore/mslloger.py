#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''

import logging
import logging.config

logging.config.fileConfig(fname="config/logger")
__logger = logging.getLogger()


def mslloger_init(level):
    global __logger

    __logger.setLevel(level)
    return __logger


def mslloger():
    global __logger
    return __logger
