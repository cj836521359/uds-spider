#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chencharles'

import PyV8

class v8Doc(PyV8.JSClass):
    def write(self, s):
        print s.decode('utf-8')

class Global(PyV8.JSClass):
    def __init__(self):
        self.document = v8Doc()

def initJsEngine():
    glob = Global()
    ctxt = PyV8.JSContext(glob)
    ctxt.enter()
    return ctxt

def eval(ctxt, js_str):
    ctxt.eval(js_str.encode('utf-8'))

