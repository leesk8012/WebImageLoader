# -*- coding: utf-8 -*-
import pycurl
import cStringIO
import sys


def get_html_data(url):
    response_buffer = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEFUNCTION, response_buffer.write)
    request_running = 1
    while request_running:
        try:
            c.perform()
            request_running = 0
        except Exception:
            print "Unexpected error:", sys.exc_info()[0]
    body = response_buffer.getvalue()
    response_buffer.close()
    return body
