# -*- coding: utf-8 -*-
import json
from htmlfile_module import html_file_write


def write_file_url(filename, url):
    data = '<br><a href=%s target="_blank"><img src=%s class="image-fullsize"/></a><br>\r\n' % (url, url)
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
            write_file_url(filename, base_url % image)
