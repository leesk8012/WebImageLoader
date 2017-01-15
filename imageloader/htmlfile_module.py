# -*- coding: utf-8 -*-


def html_file_write(filename, data):
    f = open(filename, 'a')
    f.write(data)
    f.close()
