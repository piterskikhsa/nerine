#!/usr/bin/env python
# coding: utf-8

import os
import re
import threading
import urllib.request
from xml.etree import ElementTree as ET
import NerineDB
from Logger import write_log


mydb = NerineDB.NerineDb(
        '94.243.128.141', 3306, 'nerine', 'ythbyt34', 'nerine_db', 'utf8')


def add_robots():
    new_sites = mydb.get_sites_without_pages
    thread_1 = threading.Thread(target=write_log(new_sites))
    thread_1.start()

    #print(new_sites)
    for i in new_sites[0]:
        #print(i)
        r = mydb.insert_pages_robots(i[1], i[0])
        #print(r)
        thread_2 = threading.Thread(target=write_log(r))
        thread_2.start()
        if r[0]:
            print('OK')
        else:
            print(r[0])


def parse_html(current_html_file, current_site_id, page_id):
    if re.search(r'[^\s]+robots\.txt\b', current_html_file):
        with open(current_html_file, 'r', encoding='utf-8') as f:
            for line in f:
                sitemap_link = re.search(r'^Sitemap:([\s]*[^\s]+)\s', line)
                if sitemap_link:
                    print('adding a new Sitemap link..')
                    sitemap_link = sitemap_link.group(1).strip()
                    mydb.insert_pages_newone(sitemap_link, current_site_id)
                    print(sitemap_link, 'added to the database.')
                    break
    elif re.search(r'[^\s]+\.xml\b', current_html_file):
        print('found XML:', current_html_file)
        with open(current_html_file, 'r', encoding='utf-8') as f:
            tree = ET.parse(f)

        #xmlstring = re.sub(r"""\s(xmlns="[^"]+"|xmlns='[^']+')""", '', xmlstring, count=1)


        root = tree.getroot()
        ns = root.tag[1:root.tag.index('}')]
        nsmap = {"ns": ns}

        if 'sitemapindex' in root.tag:
            for elem in root.findall('ns:sitemap', nsmap):
                if elem.find('ns:loc', nsmap).text:
                    print(elem.find('ns:loc', nsmap).text)
        elif 'urlset' in root.tag:
            for elem in root.findall('ns:url', nsmap):
                if elem.find('ns:loc', nsmap).text:
                    print(elem.find('ns:loc', nsmap).text)


    #mydb.set_pages_scantime(page_id)


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
            pass
        else:
            print('Downloaded ', url[0])
            parse_html(current_html_file, current_site_id, page_id)


def main():
    add_robots()
    download_html()

if __name__ == '__main__':
    main()
