#!/usr/bin/env python
# coding: utf-8


import os
import threading
import urllib.request
from config import db_host, db_port, db_username, db_password, db_name, db_charset
import NerineDB
from Logger import write_log
from Parser import parse_file


mydb = NerineDB.NerineDb(
        db_host , db_port, db_username, db_password, db_name, db_charset)


def add_robots():
    new_sites = mydb.get_sites_without_pages
    thread_1 = threading.Thread(target=write_log(new_sites))
    thread_1.start()

    for i in new_sites[0]:
        r = mydb.insert_pages_robots(i[1], i[0])
        thread_2 = threading.Thread(target=write_log(r))
        thread_2.start()
        if r[0]:
            print('OK')
        else:
            print(r[0])


def download_html():
    new_pages =  mydb.get_pages_without_scan

    for url in new_pages[0]:
        current_site_id = url[2]
        page_id = url[3]
        current_url = url[0].replace('http://', '').replace('/', '_')
        try:
            current_dir = os.path.join('html', str(url[1]))

            if not os.path.exists(current_dir):
                os.makedirs(current_dir)

            current_html_file = os.path.join(current_dir, current_url)
            urllib.request.urlretrieve(url[0], current_html_file)
        except Exception as e:
            print('error with url ', url[0])
            print(e)
        else:
            print('Downloaded ', url[0])
            parse_file(mydb, current_html_file, current_site_id, page_id)


def main():
    add_robots()
    download_html()

if __name__ == '__main__':
    main()
