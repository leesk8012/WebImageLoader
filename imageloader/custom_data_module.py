# -*- coding: utf-8 -*-
import json
from htmlfile_module import html_file_write
import re


def write_file_url(filename, link_url, file_url):
    data = '<br><a href=%s target="_blank"><img src=%s class="image-fullsize"/></a><br>\r\n' % (link_url, file_url)
    html_file_write(filename, data)


def write_link_url(filename, link_url):
    data = '<br><a href=%s target="_blank">%s</a><br>\r\n' % (link_url, link_url)
    html_file_write(filename, data)


def write_file_text(filename, text):
    data = '<br>%s<br>\r\n' % text
    html_file_write(filename, data)


def write_header(filename):
    data = '<html>\n<head>\n<style>div {width: 1850px;}img {max-width: 100%;}</style></head>\n<body>\n'
    html_file_write(filename, data)


def write_footer(filename):
    data = '</body>\n</html>'
    html_file_write(filename, data)


def data_parsing(filename, data, base_url):
    post_data = json.loads(data)
    for content in post_data['data']['posts']:
        for image in content['images']:
            write_file_url(filename, base_url % image, base_url % image)


def find_list_raw(data, finds):
    return data_find(data, finds)


def find_body_raw(filename, data, finds):
    urls = data_find(data, finds)
    for url in urls:
        write_file_url(filename, url, url)


def data_find(data, finds):
    result = []
    for m in re.finditer(finds, data):
        result.append(m.group(0))
    return result
