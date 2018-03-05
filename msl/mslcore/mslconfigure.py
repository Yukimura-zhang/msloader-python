#!/usr/bin/env python
# coding=utf-8

'''
msloader

@author: Yukimura.Zhang
'''

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et


class MSLConfigure():
    __conftree = et.ElementTree()

    def __init__(self, conffile):
        try:
            self.__conftree = et.ElementTree(file=conffile)
        except:
            print("[MSLConfigure] load xml failed. [conffile]%s" % conffile)
        return

    def get_common(self):
        '''
        Get common configuration.
        @return: comdic, dictionary of common configuration.
        '''
        common = self.__conftree.find('./common')

        comdic = dict()
        for elm in common:
            comdic[elm.tag] = elm.text

        return comdic

    def get_simulators(self):
        '''
        Get all simulators list.
        @return: list contain all simulators
        '''
        return self.__conftree.findall('.//simulator')

    def get_simulator(self, node):
        '''
        Get simulator's attribute and subtag value
        @return: simuattrib, attribution of the node
                 simudic, simulator dictionary
        '''
        simuattrib = node.attrib

        simudic = dict()
        for elm in node:
            simudic[elm.tag] = elm.text

        return (simuattrib, simudic)
