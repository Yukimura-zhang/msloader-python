#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''
import threading
import time
import requests

from msl.mslcore import mslloger
from msl.protocol.mpdparser import MPDParser

LIVE = 0
SHIFT = 1


class DashThread(threading.Thread):
    __logger = mslloger()
    __url = ''
    __urlroot = ''
    __mpdparser = MPDParser('')
    __dash_type = LIVE
    __mpd_update_period = 0
    __recved_length = 0
    __thread_id = 0
    __quit = False
    __vaild = True

    def __init__(self, threadid, url, type_=LIVE):
        threading.Thread.__init__(self)
        self.__thread_id = threadid
        self.__recved_length = 0
        self.__dash_type = type_
        self.__url = url
        lastslash = self.__url.rfind('/')
        self.__urlroot = self.__url[:lastslash] + '/'
        self.__quit = False
        self.__vaild = True

    def __request_slice(self, slicelst):

        for slice in slicelst:
            sliceurl = ''
            if slice[0:7] != 'http://':
                sliceurl = self.__urlroot + slice
            else:
                sliceurl = slice
            try:
                slice_r = requests.get(sliceurl, stream=True, timeout=10)
            except:
                if self.__quit != True:
                    continue
                else:
                    break

            # recv slice
            while self.__quit != True:
                try:
                    recvlen = len(slice_r.raw.read(4096))
                    if 0 < recvlen:
                        self.__recved_length += recvlen
                        self.__logger.debug('[DashThread] [%d] dash slice read %s bytes.', self.__thread_id,
                                            self.__recved_length)
                    else:
                        self.__logger.debug('[DashThread] [%d] dash slice read %s bytes. close connection.',
                                            self.__thread_id, recvlen)
                        break
                except:
                    break

            slice_r.close()
            if self.__quit != True:
                time.sleep(self.__mpd_update_period / 2)
            else:
                break

    def run(self):
        while self.__quit != True:
            try:
                mpd_r = requests.get(self.__url, stream=True, timeout=10)

                # recv mpd
                mpd = ''
                while self.__quit != True:
                    try:
                        current_recv = mpd_r.raw.read(4096)
                        current_recv_len = len(current_recv)

                        if 0 < current_recv_len:
                            mpd += str(current_recv.decode('utf-8'))
                        else:
                            break
                    except:
                        break
                mpd_r.close()

                # parse mpd
                if not self.__mpdparser.update(mpd):
                    if self.__quit != True:
                        time.sleep(1)
                        continue
                    else:
                        break

                # request slice
                self.__logger.info('[DashThread] [%d] get mpd :\n%s', self.__thread_id, mpd)
                self.__mpd_update_period = self.__mpdparser.get_update_period()
                videolst = self.__mpdparser.get_video_table()
                audiolst = self.__mpdparser.get_audio_table()

                self.__request_slice(videolst)
                self.__request_slice(audiolst)

                # after get all slice in playlist,check whether shift or not
                if SHIFT == self.__dash_type:
                    self.__logger.info(
                        '[DashThread] [%d] this is a shift request, quit cycle and do not to request mpd again.',
                        self.__thread_id, )
                    break

            except:
                continue

    def quit(self):
        self.__quit = True

    def is_vaild(self):
        return self.__vaild

    def getodsize(self):
        return self.__recved_length
