# -*- coding: utf-8 -*-

import datetime
import sys
import ConfigParser
import threading
from imageloader.custom_data_module import find_list_raw, write_footer, write_header, write_link_url, write_file_url, write_file_text
from imageloader.http_module import get_html_data

image_list = []


class ImageLoader(threading.Thread):
    def __init__(self, start, end):
        threading.Thread.__init__(self)
        self.__start = start
        self.__end = end

    def run(self):
        for page in range(self.__start, self.__end):
            data = get_html_data(PAGE_PREFIX + str(page))
            urls = find_list_raw(data, SUBJECT_REGEX)
            for url in urls:
                body_link = LINK_PREFIX + str(url.split('&')[1])
                data = get_html_data(body_link)
                images = find_list_raw(data, BODY_REGEX)
                image_list.append({'url': body_link, 'images': images, 'count': len(images)})


def init(section_name):
    global SUBJECT_REGEX
    global BODY_REGEX
    global PAGE_PREFIX
    global LINK_PREFIX

    parser = ConfigParser.ConfigParser()
    parser.read('config.ini')

    SUBJECT_REGEX = parser.get(section_name, 'SUBJECT_REGEX')
    BODY_REGEX = parser.get(section_name, 'BODY_REGEX')
    PAGE_PREFIX = parser.get(section_name, 'PAGE_PREFIX')
    LINK_PREFIX = parser.get(section_name, 'LINK_PREFIX')
    output_prefix = parser.get(section_name, 'OUTPUT_PREFIX')
    thread_num = parser.getint(section_name, 'THREAD_NUM')

    return {'output_prefix':output_prefix, 'thread_num':thread_num}


def main():
    if len(sys.argv) != 4:
        print 'Usage : %s section_name start_page end_page'
        return

    site_setting = init(sys.argv[1])
    start_page = int(sys.argv[2])
    end_page = int(sys.argv[3])
    now = datetime.datetime.now()
    filename = site_setting['output_prefix'] + "-" + now.strftime('%Y%m%d-%H%M') + ".html"
    threads = []
    page_per_thread = (end_page - start_page + 1) / site_setting['thread_num']

    for i in range(start_page, end_page, page_per_thread):
        th = ImageLoader(i, (i + page_per_thread))
        threads.append(th)
        th.start()

    for t in threads:
        t.join()

    print len(image_list)
    write_header(filename)
    for image_data in image_list:
        write_link_url(filename, image_data['url'])
        write_file_text(filename, image_data['count'])
        image_url_list = image_data['images']
        for image in image_url_list:
            write_file_url(filename, image, image)
    write_footer(filename)


if __name__ == "__main__":
    main()
