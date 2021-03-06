#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''
import threading
import requests
from msl.mslcore import mslloger

class HttpCommonThread(threading.Thread):
    __logger = mslloger()
    __recved_length = 0
    __thread_id = 0
    __url = ''
    __range = ''
    __r = None
    __quit = False
    __vaild = True
    __title = ''
    __headers = ''

    def __init__(self, threadid, url, title, simu_attrib={}, simu_dic={}):
        threading.Thread.__init__(self)
        self.__url = url
        self.__thread_id = threadid
        self.__title = title
        self.__recved_length = 0
        self.__quit = False

        if simu_attrib == {}:
            self.__headers = ''
        else:
            try:
                if simu_attrib['seek'] == 'range':
                    self.__range = simu_dic['range']
                    self.__headers = {'Range': self.__range}
                else:
                    self.__headers = ''
            except:
                self.__headers = ''

                self.__private_connect()

    def __private_connect(self):
        if self.__headers != '':
            try:
                self.__r = requests.get(self.__url, headers=self.__headers, stream=True, timeout=10)
            except:
                self.__vaild = False
        else:
            try:
                self.__r = requests.get(self.__url, stream=True, timeout=10)
            except:
                self.__vaild = False

    def run(self):
        while self.__quit != True:
            try:
                recvlen = len(self.__r.raw.read(4096))
                if 0 < recvlen:
                    self.__recved_length += recvlen
                    self.__logger.debug('[HttpCommonThread] [%d] [%s] read %s bytes.',
                                        self.__thread_id, self.__title, self.__recved_length)
                else:
                    self.__logger.debug('[HttpCommonThread] [%d] [%s] read %s bytes. close connection.',
                                        self.__thread_id, self.__title, recvlen)
                    break
            except:
                break

        self.__r.close()

    def quit(self):
        self.__quit = True

    def is_vaild(self):
        return self.__vaild

    def getodsize(self):
        return self.__recved_length
