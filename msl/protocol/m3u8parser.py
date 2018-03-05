#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''
from msl.mslcore import mslloger

EXTM3U = "#EXTM3U"
EXT_X_MEDIA_SEQUENCE = "#EXT-X-MEDIA-SEQUENCE"
EXT_X_TARGETDURATION = "#EXT-X-TARGETDURATION"
EXTINF = "#EXTINF"


class M3U8Parser(object):
    __logger = mslloger()
    __m3u8 = ''
    __parse_success = False
    __kvdict = {}
    __playlist = []
    __target_duration = ''
    __sequence = ''

    def __init__(self, m3u8):
        self.update(m3u8, False)

    def __reset(self):
        self.__m3u8 = ""
        self.__parse_success = False
        self.__kvdict = {}
        self.__playlist = []

    def __verify(self):
        if self.__m3u8[0:len(EXTM3U)] == EXTM3U:
            # self.__logger.debug("[M3U8Parser] __verify success.");
            return True
        else:
            self.__logger.error('[M3U8Parser] __verify failed. [self.__m3u8[0:7]]%s', self.__m3u8[0:len(EXTM3U)])
            return False

    def __parse(self):
        linelst = self.__m3u8.splitlines()

        for line in linelst:

            # parse playlist
            if line[0] != '#':
                self.__playlist.append(line)
                continue

            # parse k-v lines
            kv = line.split(':')
            if len(kv) != 2:
                continue
            self.__kvdict[kv[0].strip()] = kv[1].strip()

        try:
            self.__target_duration = self.__kvdict[EXT_X_TARGETDURATION]
            self.__sequence = self.__kvdict[EXT_X_MEDIA_SEQUENCE]
        except KeyError:
            self.__parse_success = False
            return

        if 0 == len(self.__playlist) or self.__playlist == None:
            self.__parse_success = False
            return

        self.__parse_success = True

    def update(self, m3u8, verify=True):
        self.__reset()
        self.__m3u8 = m3u8
        if verify:
            if not self.__verify():
                return False
        self.__parse()
        return True

    def get_target_duration(self):
        if self.__parse_success:
            return int(self.__target_duration)

    def get_sequence(self):
        if self.__parse_success:
            return int(self.__sequence)

    def get_playlist(self):
        if self.__parse_success:
            return self.__playlist
