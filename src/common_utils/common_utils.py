# -*- coding: utf-8 -*-
"""
工具类，维护一些通用方法
"""
__author__ = "songlihua"

import codecs
import json
import sys
import csv

replace_str = ["\\", "/", "\"", ":", "*", "?", "", "<", ">", "|", "         "]
down_type = [".doc", "docx", "xls", "xlsx", "ppt", "pptx", "dps","et", "wps", "txt", "rtf", "ini", "gif", "jpg", "bmp", "tif", "png","tiff", "jpeg", "pdf"]


def write_to_file_with_stream(str_data, filename):
    file_object = None
    try:
        file_object = codecs.open(filename, "wb")
        file_object.write(str_data)
    finally:
        file_object.close()

def write_to_file(str_data, filename):
    file_object = ""
    try:
        file_object = codecs.open(filename, "w", "utf-8-sig")
        str_data = str_data.decode()
        file_object.write(str_data)
    finally:
        file_object.close()

def append_to_file(str_data,filename):
    file_object = ""
    try:
        file_object = codecs.open(filename,'ab','utf-8-sig')
        str_data = str_data.decode()
        file_object.write(str_data)
    finally:
        file_object.close()


def beautify_json(ugly_json):
    # ensure_ascii在处理utf-8的时候必须
    return json.dumps(ugly_json, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))


def load_json(json_file_name):
    original_file_object = codecs.open(json_file_name, "r", "utf-8-sig")
    return json.loads(original_file_object.read())


def write_json(json_data, json_file_name):
    write_to_file(beautify_json(json_data), json_file_name)


def read_file_content(file_name):
    return codecs.open(file_name, "r", "utf-8-sig").read()



def merge_csv(src, dest):
    with codecs.open(dest,'ab','utf-8-sig') as outcsv:
        out = csv.writer(outcsv)
        with codecs.open(src,'r','utf-8-sig') as incsv:
            sales = csv.reader(incsv)
            out.writerows(sales)
            incsv.close()
        outcsv.close()


