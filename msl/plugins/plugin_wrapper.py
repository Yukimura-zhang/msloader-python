#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''

from msl.protocol.http_common import *
from msl.protocol.rtmp import *
from msl.protocol import hls
from msl.protocol.hls import HLSThread
from msl.protocol import dash
from msl.protocol.dash import DashThread


class plugin_wrapper(object):
    __clicount = 0
    __url = ''
    __tlist = []
    __title = ''
    __odsize = 0

    def __init__(self, url, title, clicount, simu_attrib={}, simu_dic={}):
        self.__clicount = int(clicount)
        self.__url = url
        self.__title = title
        self.__tlist = []
        self.__odsize = 0

        if self.__title.find('@rtmp') > 0:
            for index in range(self.__clicount):
                flv = RtmpThread(index, self.__url)
                if flv.is_vaild():
                    flv.start()
                    self.__tlist.append(flv)

        elif self.__title.find('@hls') > 0:
            if self.__title.find('shift@') < 0:
                for index in range(self.__clicount):
                    flv = HLSThread(index, self.__url)
                    if flv.is_vaild():
                        flv.start()
                        self.__tlist.append(flv)
            else:
                for index in range(self.__clicount):
                    flv = HLSThread(index, self.__url, hls.SHIFT)
                    if flv.is_vaild():
                        flv.start()
                        self.__tlist.append(flv)

        elif self.__title.find('@dash') > 0:
            if self.__title.find('shift@') < 0:
                for index in range(self.__clicount):
                    flv = DashThread(index, self.__url)
                    if flv.is_vaild():
                        flv.start()
                        self.__tlist.append(flv)
            else:
                for index in range(self.__clicount):
                    flv = DashThread(index, self.__url, dash.SHIFT)
                    if flv.is_vaild():
                        flv.start()
                        self.__tlist.append(flv)

        else:
            for index in range(self.__clicount):
                flv = HttpCommonThread(index, self.__url, self.__title, simu_attrib, simu_dic)
                if flv.is_vaild():
                    flv.start()
                    self.__tlist.append(flv)

    def getruninfo(self):
        # return title,alive cnt,and total output size
        cnt = 0
        odsize = 0
        for flv in self.__tlist:
            if flv.is_alive():
                cnt += 1
            #do getodsize() even thread not alive
            odsize += flv.getodsize()

        self.__odsize = odsize
        return self.__title, cnt, self.__odsize

    def quittest(self):
        for flv in self.__tlist:
            flv.quit()
            flv.join()
        print('plugin_wrapper for [%s] quit' % (self.__title))
