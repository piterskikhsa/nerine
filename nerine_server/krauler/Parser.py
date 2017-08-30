#!/usr/bin/env python
# coding: utf-8

import os
import re
from xml.etree import ElementTree as ET
from urllib.parse import quote


def parse_robots(robots_file, site_id, mydb):
    print('found robots.txt:', robots_file)
    with open(robots_file, 'r', encoding='utf-8') as f:
        for line in f:
            sitemap_link = re.search(r'^[S|s]itemap:([\s]*[^\s]+)\s', line)
            if sitemap_link:
                print('adding a new Sitemap link..')
                sitemap_link = sitemap_link.group(1).strip()
                mydb.insert_pages_newone(sitemap_link, site_id)
                print(sitemap_link, 'added to the database.')
                break


def parse_url(url):
    url_1 = re.search(r'^[^=]+=', url)
    url_2 = re.search(r'=([^\s]+)', url)
    if url_1 and url_2:
        return '{}{}'.format(url_1.group(), quote(url_2.group(1)))


def make_path_to_file(page_url, site_name):
    file = page_url
    print('parsing url..', page_url)
    replacements = ('http://', 'https://', '?', '*', '"', ">", "<", "\\", ":", "|")
    for r in replacements:
        file = file.replace(r, '')
    file = file.replace('/', '_')
    current_dir = os.path.join('html', str(site_name))

    if not os.path.exists(current_dir):
        os.makedirs(current_dir)

    path_to_file = os.path.join(current_dir, file)
    return path_to_file


def parse_xml_sitemap(xml_file, site_id, mydb):
    print('parsing.. a xml-sitemap:', xml_file)
    with open(xml_file, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)

    root = tree.getroot()
    ns = root.tag[1:root.tag.index('}')]
    nsmap = {"ns": ns}

    if 'sitemapindex' in root.tag:
        for elem in root.findall('ns:sitemap', nsmap):
            embedded_xml_file = elem.find('ns:loc', nsmap).text
            if embedded_xml_file:
                if re.search(r'[^\s]+\.xml\b', embedded_xml_file):
                    print('found the embedded xml file:', embedded_xml_file)
                    mydb.insert_pages_newone(embedded_xml_file, site_id)
                    print(embedded_xml_file, 'added to the database.')
    elif 'urlset' in root.tag:
        for elem in root.findall('ns:url', nsmap):
            try:
                html_file = elem.find('ns:loc', nsmap).text
            except Exception as e:
                print('Error:', e)
            else:
                print('found a html file:', html_file)
                mydb.insert_pages_newone(html_file, site_id)
                print(html_file, 'added to the database.')


def parse_txt_sitemap(txt_sitemap, site_id, mydb):
    print('parsing a txt-sitemap')
    with open(txt_sitemap, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if re.search(r'^http[s]{0,1}:[/]{2}[\w]+[^\s]+', line):
                line = line.strip()
                print('found a html file:', line)
                mydb.insert_pages_newone(line, site_id)
                print(line, 'added to the database.')


def parse_html(html_file, site_id, page_id, mydb, persons_dictionary, seek_words):
    def find_person_id(word):
        for id, word_list in persons_dictionary.items():
            if word in word_list:
                return id

    with open(html_file, 'r', encoding='utf-8') as f:
        html_words = f.read().split()

    page_rank_dict = {}

    print('seeking words...')
    for word in html_words:
        if word in seek_words:
            if find_person_id(word) not in page_rank_dict:
                page_rank_dict[find_person_id(word)] = 1
            else:
                page_rank_dict[find_person_id(word)] += 1

    for person_id, rank in page_rank_dict.items():
        result = mydb.set_person_page_rank(person_id, page_id, rank)
        if result[0]:
            print('added page rank (person_id, page_id, rank):', person_id, page_id, rank)