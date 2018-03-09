#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''

import logging,logging.config
import cloghandler
#pip install ConcurrentLogHandler #
# for "have multiple instances all running at the same time and writing to the same log file"


logging.config.fileConfig(fname="config/logger")
__logger = logging.getLogger()


def mslloger_init(level):
    global __logger

    __logger.setLevel(level)
    return __logger


def mslloger():
    global __logger
    return __logger
