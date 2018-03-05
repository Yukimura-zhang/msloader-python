#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''
import time
import re

from msl.mslcore import mslloger
from msl.mslcore.mslconfigure import MSLConfigure
from msl.mslcore.mslloger import mslloger_init
from msl.plugins import *

mslconfigure = MSLConfigure('./config/msloader.xml')


def test_main():
    global mslconfigure

    comdic = mslconfigure.get_common()
    mslloger_init(comdic["loglevel"])
    testtime = comdic["testtime"]

    logger = mslloger()

    simus = mslconfigure.get_simulators()
    vaild_simus = []

    for simu in simus:
        simuattrib, simudic = mslconfigure.get_simulator(simu)

        enable = simuattrib['enable']
        plugin = simuattrib['plugin']

        if not enable == 'true':
            continue

        logger.debug("[MAIN] [plugin]%s[url]%s[number]%s", plugin, simudic["url"], simudic["number"])
        p = plugin_wrapper(simudic["url"], plugin, simudic["number"], simuattrib, simudic)
        vaild_simus.append(p)

    if len(vaild_simus) < 1:
        print("No vaild simulators,quit!")
        return

    if re.compile("^[0-9]*$").match(testtime):
        time.sleep(int(testtime))
    else:
        time.sleep(600)

    for p in vaild_simus:
        p.quittest()

    return
