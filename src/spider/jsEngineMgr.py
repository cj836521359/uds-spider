# -*- coding: utf-8 -*-
__author__ = 'chencharles'


from __init__ import *
import sys
import time
import chardet
import urllib
import PyV8
#import jsEngineMgr
import globalconf


if __name__ == '__main__':
    print 'x'


def initJsEngine():
    ctxt = PyV8.JSContext()
    ctxt.enter()
    return ctxt


#def eval(jscontent):

    #print 'jscontent'
