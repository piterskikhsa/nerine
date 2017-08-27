#!/usr/bin/env python
# coding: utf-8


from xml.etree import ElementTree as ET


def parse_robots(robots_file, site_id, mydb):
    print('found robots.txt:', robots_file)
    with open(robots_file, 'r', encoding='utf-8') as f:
        for line in f:
            sitemap_link = re.search(r'^Sitemap:([\s]*[^\s]+)\s', line)
            if sitemap_link:
                print('adding a new Sitemap link..')
                sitemap_link = sitemap_link.group(1).strip()
                mydb.insert_pages_newone(sitemap_link, site_id)
                print(sitemap_link, 'added to the database.')
                break


def parse_xml(xml_file, site_id, mydb):
    print('found XML:', xml_file)
    with open(xml_file, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)

    root = tree.getroot()
    ns = root.tag[1:root.tag.index('}')]
    nsmap = {"ns": ns}

    if 'sitemapindex' in root.tag:
        for elem in root.findall('ns:sitemap', nsmap):
            if elem.find('ns:loc', nsmap).text:
                print(elem.find('ns:loc', nsmap).text)
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


def parse_html(html_file, site_id, page_id, mydb, persons_dictionary, seek_words):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_words = f.read().split()

    print('seeking words...')
    for word in html_words:
        if word in seek_words:
            print('FOUND THE WORD:', word)