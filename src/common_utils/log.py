#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chencharles'


import logging
import sys

def init_log(log_name):
    logger = logging.getLogger('spiderlog')
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    file_handler = logging.FileHandler(log_name)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger



