#!/usr/bin/env python
# coding: utf-8

import os
import re
import string
from xml.etree import ElementTree as ET
from urllib.parse import quote
import Logger


def parse_robots(robots_file, site_id, mydb):
    disallow_list = []
    Logger.logger.info('parsing robot: %s', robots_file)
    with open(robots_file, 'r', encoding='utf-8') as f:
        for line in f:
            sitemap_link = re.search(r'^[S|s]itemap:([\s]*[^\s]+)\s', line)
            if sitemap_link:
                sitemap_link = sitemap_link.group(1).strip()
                if not mydb.check_if_page_exists(sitemap_link):
                    mydb.insert_pages_newone(sitemap_link, site_id)
                return [True, disallow_list]

            # catching disallow strings and making regex
            disallow_line = re.search(r'^[D|d]isallow:([\s]*[^\s]+)\s', line)
            if disallow_line:
                disallow_line = disallow_line.group(1).strip()
                if disallow_line == '/' or disallow_line == '/*':
                    disallow_line = '.+?'
                else:
                    disallow_line = disallow_line.replace('.', '\.').replace('*', '.+?')
                disallow_list.append(disallow_line)
    return [False, disallow_list]


def is_allowed_by_robots(disallow_list, page):
    for i in disallow_list:
        if re.search(r'{}'.format(i), page):
            return False
    return True


def parse_url(url):
    url_1 = re.search(r'^[^=]+=', url)
    url_2 = re.search(r'=([^\s]+)', url)
    if url_1 and url_2:
        return '{}{}'.format(url_1.group(), quote(url_2.group(1)))


def is_valid_url(url):
    if re.search(r"^((?:http)s?://)?(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?$))",
                 url, re.IGNORECASE):
        return True
    else:
        return False


def make_path_to_file(page_url, site_name):
    file = page_url
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
    Logger.logger.info('parsing XML: %s', xml_file)
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
                    if not mydb.check_if_page_exists(embedded_xml_file):
                        mydb.insert_pages_newone(embedded_xml_file, site_id)
    elif 'urlset' in root.tag:
        for elem in root.findall('ns:url', nsmap):
            try:
                html_file = elem.find('ns:loc', nsmap).text
            except Exception as error:
                Logger.logger.error('could not find an urlset in XML: %s', error)
            else:
                if not mydb.check_if_page_exists(html_file):
                    mydb.insert_pages_newone(html_file, site_id)


def parse_txt_sitemap(txt_sitemap, site_id, mydb):
    Logger.logger.info('parsing a sitemap.txt: %s', txt_sitemap)
    with open(txt_sitemap, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if re.search(r'^http[s]{0,1}:[/]{2}[\w]+[^\s]+', line):
                line = line.strip()
                if not mydb.check_if_page_exists(line):
                    mydb.insert_pages_newone(line, site_id)


def parse_html(html_file, site_id, page_id, mydb, persons_dictionary, seek_words):
    def find_person_id(word):
        for id, word_list in persons_dictionary.items():
            if word in word_list:
                return id

    with open(html_file, 'r', encoding='utf-8') as f:
        html_words = f.read().lower()

    html_words = re.sub('<.*?>', ' ', html_words)

    for s in string.punctuation:
        html_words = html_words.replace(s, ' ')

    html_words = html_words.split()
    html_words = list(map(lambda x: x.strip(), html_words))

    page_rank_dict = {}
    Logger.logger.info('seeking words in %s ...', html_file)

    for word in html_words:
        if word in seek_words:
            if find_person_id(word) not in page_rank_dict:
                page_rank_dict[find_person_id(word)] = 1
            else:
                page_rank_dict[find_person_id(word)] += 1

    for person_id, rank in page_rank_dict.items():
        result = mydb.set_person_page_rank(person_id, page_id, rank)
        if result:
            Logger.logger.info('added page rank (personID, PageID, Rank): %s %s %s', person_id, page_id, rank)
