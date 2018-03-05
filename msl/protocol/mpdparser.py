#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''

'''
This 'mpdparser' just parse 'minimumUpdatePeriod' and A/V slice list.
Here is a DASH index file example, index.mpd
Create by ms3 stream media server.
@reference:
Wiki - https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP
ISO doc - http://standards.iso.org/ittf/licence.html
'''
'''
<?xml version="1.0"?>
<MPD
    type="dynamic"
    xmlns="urn:mpeg:dash:schema:mpd:2011"
    availabilityStartTime="2015-09-17T13:15:21+08:00"
    availabilityEndTime="2015-09-17T13:15:56+08:00"
    minimumUpdatePeriod="PT5S"
    minBufferTime="PT5S"
    timeShiftBufferDepth="PT0H0M0.00S"
    suggestedPresentationDelay="PT10S"
    profiles="urn:hbbtv:dash:profile:isoff-live:2012,urn:mpeg:dash:profile:isoff-live:2011"
    xmlns:xsi="http://www.w3.org/2011/XMLSchema-instance"
    xsi:schemaLocation="urn:mpeg:DASH:schema:MPD:2011 DASH-MPD.xsd">
  <Period start="PT0S" id="dash">
    <AdaptationSet
        id="1"
        segmentAlignment="true"
        maxWidth="720"
        maxHeight="576"
        maxFrameRate="0">
      <Representation
          id="_H264"
          mimeType="video/mp4"
          codecs="avc1.4d401e"
          width="720"
          height="576"
          frameRate="0"
          sar="1:1"
          startWithSAP="1"
          bandwidth="0">
        <SegmentTemplate
            presentationTimeOffset="0"
            timescale="1000"
            media="slice/$Time$.m4v"
            initialization="init.m4v">
          <SegmentTimeline>
             <S t="1464480017" d="6040"/>
             <S t="1464486057" d="6000"/>
             <S t="1464492057" d="5200"/>
             <S t="1464497257" d="6280"/>
             <S t="1464503537" d="6760"/>
             <S t="1464510297" d="5360"/>
          </SegmentTimeline>
        </SegmentTemplate>
      </Representation>
    </AdaptationSet>
    <AdaptationSet
        id="2"
        segmentAlignment="true">
      <AudioChannelConfiguration
          schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011"
          value="1"/>
      <Representation
          id="_AAC"
          mimeType="audio/mp4"
          codecs="mp4a.40.2"
          audioSamplingRate="48000"
          startWithSAP="1"
          bandwidth="0">
        <SegmentTemplate
            presentationTimeOffset="0"
            timescale="1000"
            media="slice/$Time$.m4a"
            initialization="init.m4a">
          <SegmentTimeline>
             <S t="1464480017" d="6040"/>
             <S t="1464486057" d="6000"/>
             <S t="1464492057" d="5200"/>
             <S t="1464497257" d="6280"/>
             <S t="1464503537" d="6760"/>
             <S t="1464510297" d="5360"/>
          </SegmentTimeline>
        </SegmentTemplate>
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
'''

from msl.mslcore import mslloger

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et


class MPDParser(object):
    __logger = mslloger()
    __mpdtreeroot = None

    __update_period = 5
    __video_table = []
    __audio_table = []

    def __init__(self, mpd):
        self.__parse(mpd)
        return

    def __parse(self, mpd):
        try:
            self.__mpdtreeroot = et.fromstring(mpd)
            rootattribdic = self.__mpdtreeroot.attrib
            speriod = rootattribdic['minimumUpdatePeriod']
            self.__update_period = int(speriod[len('PT'): speriod.find('S')])

            lst = self.__mpdtreeroot.findall('.//{urn:mpeg:dash:schema:mpd:2011}S')
            for elm in lst:
                elmdic = elm.attrib
                self.__video_table.append('/slice/' + elmdic["t"] + '.m4v')
                self.__audio_table.append('/slice/' + elmdic["t"] + '.m4a')

        except:
            self.__logger.error("[MPDParser] __parse failed.")
            return

    def get_update_period(self):
        return self.__update_period

    def get_video_table(self):
        return self.__video_table

    def get_audio_table(self):
        return self.__audio_table
