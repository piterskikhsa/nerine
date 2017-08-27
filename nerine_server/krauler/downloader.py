#!/usr/bin/env python
# coding: utf-8


import os
import threading
import re
import urllib.request
from config import db_host, db_port, db_username, db_password, db_name, db_charset
import NerineDB
from Logger import write_log
from Parser import parse_robots, parse_xml, parse_html


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


def get_file(url, file):
    try:
        urllib.request.urlretrieve(url, file)
    except Exception as e:
        print(e)
    else:
        print('got', url)


def get_html_file(url, file):
    req = urllib.request.urlopen(url)
    try:
        charset = req.info().get_content_charset()
    except Exception as e:
        print(e)
        content = req.read().decode('utf-8')
    else:
        content = req.read().decode(charset)
        print('charset =', charset)
    finally:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print('got', url)

def download_html():
    new_pages =  mydb.get_pages_without_scan

    for url in new_pages[0]:
        current_url = url[0]
        site_id = url[2]
        page_id = url[3]
        file = url[0].replace('http://', '').replace('/', '_')
        current_dir = os.path.join('html', str(url[1]))
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)

        file = os.path.join(current_dir, file)

        if re.search(r'[^\s]+robots\.txt\b', current_url):
            get_file(current_url, file)
            parse_robots(file, site_id, mydb)
        elif re.search(r'[^\s]+\.xml\b', current_url):
            get_file(current_url, file)
            parse_xml(file, site_id, mydb)
        else:
            get_html_file(current_url, file)
            parse_html(file, site_id, page_id, mydb, persons_dictionary, seek_words)

        #mydb.set_pages_scantime(page_id)


def main():
    global persons_dictionary
    global seek_words

    persons_dictionary = mydb.get_persons[0]
    seek_words = []

    for pair in persons_dictionary.items():
        seek_words.extend(pair[1])

    add_robots()
    download_html()

if __name__ == '__main__':
    main()
