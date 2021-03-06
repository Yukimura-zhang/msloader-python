#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''
'''
@refrence: http://pythonhosted.org/python-librtmp/
You need install librtmp first.
Get python-librtmp pakage:
git clone git://github.com/chrippa/python-librtmp.git
'''

import librtmp
import threading
from msl.mslcore import mslloger


class RtmpThread(threading.Thread):
    __logger = mslloger()
    __recved_length = 0
    __thread_id = 0
    __quit = False
    __vaild = True
    __url = ''

    def __init__(self, threadid, url):
        threading.Thread.__init__(self)
        self.__thread_id = threadid
        self.__recved_length = 0
        self.__quit = False
        self.__url = url

        self.__private_connect()

    def __private_connect(self):
        try:
            # Create a connection
            self.__rtmp_conn = librtmp.RTMP(self.__url, live=True, timeout=10)
            # Attempt to connect
            self.__rtmp_conn.connect()
            # Get a file-like object to access to the stream
            self.__rtmp_stream = self.__rtmp_conn.create_stream()

        except:
            self.__logger.error("[RtmpThread] librtmp initialize failed.")
            self.__vaild = False

    def run(self):
        while self.__quit != True:
            try:
                recvlen = len(self.__rtmp_stream.read(4096))
                if recvlen > 0:
                    self.__recved_length += recvlen
                    self.__logger.debug('[RtmpThread] [%d] rtmp have read %s bytes.',
                                        self.__thread_id, self.__recved_length)
                else:
                    self.__logger.debug('[RtmpThread] [%d] read %s bytes. close connection.',
                                        self.__thread_id, recvlen)
                    break
            except:
                self.__logger.debug('[RtmpThread] [%d] rtmp read error.', self.__thread_id)
                break
        self.__rtmp_stream.close()

    def quit(self):
        self.__quit = True

    def is_vaild(self):
        return self.__vaild

    def getodsize(self):
        return self.__recved_length
