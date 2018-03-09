#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''
import time
import re
from concurrent.futures import ProcessPoolExecutor,as_completed
import os

from msl.mslcore import mslloger
from msl.mslcore.mslconfigure import MSLConfigure
from msl.mslcore.mslloger import mslloger_init
from msl.plugins import *

mslconfigure = MSLConfigure('./config/msloader.xml')
sleept = 10

def run_simulator(simus, loglevel,timeout):
    pid = os.getpid()
    if len(simus) < 1:
        ret = '[Process:%s] Do not get simulators from msloader.xml' + pid
        return ret

    global sleept
    mslloger_init(loglevel)
    logger = mslloger()
    vaild_simus = []

    for simu in simus:
        simuattrib, simudic = mslconfigure.get_simulator(simu)

        enable = simuattrib['enable']
        plugin = simuattrib['plugin']

        if not enable == 'true':
            continue

        if re.compile("^[0-9]*$").match(simudic["number"]):
            logger.debug("[MAIN] [plugin]%s[url]%s[number]%s", plugin, simudic["url"], simudic["number"])
            p = plugin_wrapper(pid,simudic["url"], plugin, simudic["number"], simuattrib, simudic)
            vaild_simus.append(p)

    if len(vaild_simus) < 1:
        ret = '[Process:%s] No vaild simulators,quit!' + (pid)
        return ret

    duration = 0
    while duration < timeout:
        mint = min(sleept, (timeout - duration))
        time.sleep(mint)
        duration += mint

        for p in vaild_simus:
            title, cnt, tsize, delta = p.getruninfo()
            print('[Process:%s] plugin_wrapper for [%s] have [%d]threads alive,total data szie = [%d],bitrate is [%d kbps]' \
                  % (title, cnt, tsize, (delta / mint / 1000),pid))
        print('==================================================================')

    for p in vaild_simus:
        p.quittest()

    ret = '[Process:%s] All simulators have done!' + (pid)
    return ret


def test_main():
    global mslconfigure

    comdic = mslconfigure.get_common()
    try:
        loglevel = comdic["loglevel"]
    except:
        loglevel = 'DEBUG'

    try:
        testtime = comdic["testtime"]
        if re.compile("^[0-9]*$").match(testtime):
            timeout = int(testtime)
        else:
            timeout = 600
    except:
        timeout = 600

    try:
        workernum = comdic["workernum"]
        if re.compile("^[0-9]*$").match(workernum):
            workernum = int(workernum)
        else:
            workernum = 2
    except:
        workernum = 2

    simus = mslconfigure.get_simulators()

    with ProcessPoolExecutor(max_workers=workernum) as executor:
        feature_to_simulator = {executor.submit(run_simulator, simus, loglevel, timeout):\
                i for i in range(workernum)}

        for future in as_completed(feature_to_simulator):
            simulator = feature_to_simulator[future]
            try:
                result = future.result()
            except Exception as e:
                print('raise an exception: {}'.format(e))
            else:
                print('')

    return
