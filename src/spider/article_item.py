#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chencharles'

import os

class article_item:
    def __init__(self, article_url, title, public_time):
        self.article_url = article_url
        self.title = title
        self.public_time = public_time

    def set_section_name(self, section_name):
        self.section_name = section_name

