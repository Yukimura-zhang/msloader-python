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
from msl.protocol.m3u8parser import M3U8Parser

LIVE = 0
SHIFT = 1


class HLSThread(threading.Thread):
    __logger = mslloger()
    __url = ''
    __urlroot = ''
    __m3u8parser = M3U8Parser('')
    __hls_type = LIVE
    __m3u8_sequence = 0
    __recved_length = 0
    __thread_id = 0
    __m3u8_target_duration = 0
    __quit = False
    __vaild = True

    def __init__(self, threadid, url, type_=LIVE):
        threading.Thread.__init__(self)
        self.__thread_id = threadid
        self.__recved_length = 0
        self.__hls_type = type_
        self.__url = url
        lastslash = self.__url.rfind('/')
        self.__urlroot = self.__url[:lastslash] + '/'
        self.__quit = False
        self.__vaild = True

    def __request_slice(self, playlist):
        for slice in playlist:
            sliceurl = ""
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
                        self.__logger.debug('[HLSThread] [%d] hls slice read %s bytes.', self.__thread_id,
                                            self.__recved_length)
                    else:
                        self.__logger.debug('[HLSThread] [%d] hls slice read %s bytes. close connection.', self.__thread_id,
                                            recvlen)
                        break
                except:
                    break
            slice_r.close()

            if self.__quit != True:
                time.sleep(self.__m3u8_target_duration / 2)
            else:
                break

    def run(self):
        while self.__quit != True:
            try:
                m3u8_init_r = requests.get(self.__url, allow_redirects=False, stream=True, timeout=10)
                try:
                    # may be no this item
                    red_location = m3u8_init_r.headers["Location"]
                except:
                    red_location = ""
                if "" != red_location:
                    lastslash = red_location.rfind('/')
                    self.__urlroot = red_location[:lastslash] + '/'
                    self.__logger.debug('[HLSThread] [%d] update [__urlroot]%s', self.__thread_id, self.__urlroot)

                # recv m3u8
                m3u8_r = requests.get(self.__url, allow_redirects=True, stream=True, timeout=10)
                m3u8 = ''
                while self.__quit != True:
                    try:
                        current_recv = m3u8_r.raw.read(4096)
                        current_recv_len = len(current_recv)
                        if 0 < current_recv_len:
                            m3u8 += str(current_recv.decode('utf-8'))
                        else:
                            break
                    except:
                        break
                m3u8_r.close()

                # parse m3u8
                if not self.__m3u8parser.update(m3u8):
                    if self.__quit != True:
                        time.sleep(1)
                        continue
                    else:
                        break


                # request slice
                self.__logger.info('[HLSThread] [%d] get m3u8 :\n%s', self.__thread_id, m3u8)
                self.__m3u8_sequence = self.__m3u8parser.get_sequence()
                self.__m3u8_target_duration = self.__m3u8parser.get_target_duration()
                playlist = self.__m3u8parser.get_playlist()

                self.__request_slice(playlist)

                # after get all slice in playlist,check whether shift or not
                if SHIFT == self.__hls_type:
                    self.__logger.info(
                        '[HLSThread] [%d] this is a shift request, quit cycle and do not to request m3u8 again.',
                        self.__thread_id)
                    break
            except:
                continue

    def quit(self):
        self.__quit = True

    def is_vaild(self):
        return self.__vaild

    def getodsize(self):
        return self.__recved_length