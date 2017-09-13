#!/usr/bin/env python3.5
# coding: utf-8


import re
import urllib.request
import gzip
from bs4 import BeautifulSoup
from config import db_host, db_port, db_username, db_password, db_name, db_charset
import NerineDB
import  Logger
from Parser import parse_robots, parse_xml_sitemap, parse_html, make_path_to_file,\
    parse_url, parse_txt_sitemap, is_valid_url, is_allowed_by_robots


mydb = NerineDB.NerineDb(
            db_host , db_port, db_username, db_password, db_name, db_charset)


def add_robots():
    new_sites = mydb.get_sites_without_pages
    for site in new_sites:
        if mydb.insert_pages_robots(site[1], site[0]):
            Logger.logger.info('new robots page inserted.')
        else:
            Logger.logger.error('could not insert robots.txt for %s', site)


def get_file(url, file):
    try:
        Logger.logger.info('getting a file... %s', url)
        urllib.request.urlretrieve(url, file)
    except Exception as error:
        Logger.logger.error('could not get: %s. output: %s', url, error)
        return False
    else:
        Logger.logger.info('GOT: %s. PUT it to %s', url, file)
        return True


def get_html_file(url, file_path):
    Logger.logger.info('getting a html file %s:', url)
    if '?' and '=' in url:
        url = parse_url(url)
    try:
        Logger.logger.info('found http GET request. parsing params..')
        req = urllib.request.urlopen(url)
    except Exception as error:
        Logger.logger.error('could not get %s: output: %s', url, error)
        return False
    else:
        try:
            Logger.logger.info('checking content-type..')
            content_type = req.info().get_content_subtype()
        except Exception as error:
            Logger.logger.error('could not get %s', error)
            return False
        else:
            if re.search(r'[html|HTML]', content_type):
                try:
                    charset = req.info().get_content_charset()
                except Exception as error:
                    Logger.logger.error('could not determine charset. %s . going to use utf-8..', error)
                    content = req.read().decode('utf-8')
                else:
                    try:
                        content = req.read().decode(charset)
                    except Exception as error:
                        Logger.logger.error('could not decode %s %s', url, error)
                        content = req.read().decode('utf-8')
                    Logger.logger.info('charset is %s', charset)
                finally:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    Logger.logger.info('GOT %s', url)

                return True
            else:
                Logger.logger.error('%s has a bad content-type: %s', url, content_type)
                return False


def ungzip_file(gz_file):
        out_xml_file = gz_file[:-3]
        try:
            with gzip.open(gz_file, 'rb') as f:
                content = f.read()
        except Exception as error:
            Logger.logger.error('could not decompress %s . output: %s', gz_file, error)
            return False
        else:
            try:
                with open(out_xml_file, 'wb') as f2:
                    f2.write(content)
            except Exception as error:
                Logger.logger.info('could not open %s . output: %s', out_xml_file, error)
            else:
                Logger.logger.info('%s was succesfully decompressed.', gz_file)
                return True


def insert_and_parse_page(path_to_html_file, site_id, mydb, persons_dictionary, seek_words, new_link):
    page_id = mydb.check_if_page_exists(new_link)

    if not page_id:
        page_id = mydb.insert_pages_newone(new_link, site_id)[1]

    if page_id > 0:
        parse_html(path_to_html_file, site_id, page_id, mydb, persons_dictionary, seek_words)
        mydb.set_pages_scantime(page_id)
        Logger.logger.info('%s parsed.', new_link)


def is_internal_link(url, site_name):
    new_link = re.sub(r'https?://', '', url, re.IGNORECASE)
    new_link = re.sub(r'[/|?]{1}[^/]+$', '', new_link)
    if re.search(r'([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}', new_link):
            if re.search(r'\b{}\b'.format(site_name), new_link):
                return True
    return False


def get_and_parse_whole_site(site_name, site_id, disallow_list, page='', already_parsed_pages=[]):
    if page == '':
        path_to_file = make_path_to_file(site_name, site_name)
        url = ''.join(['http://', site_name])
    else:
        path_to_file = make_path_to_file(page, site_name)
        url = page

    if get_html_file(url, path_to_file):
        insert_and_parse_page(path_to_file, site_id, mydb, persons_dictionary, seek_words, url)
        already_parsed_pages.append(url)

        soup = BeautifulSoup(open(path_to_file, 'r', encoding='utf-8'), 'html.parser')
        for link in soup.find_all('a', href = True):
            new_link = link['href']
            if not is_internal_link(new_link, site_name):
                continue

            first_part_link = re.sub(r'/[^/]+$', '', new_link)

            if re.search(r'^/[^\s^]+$', first_part_link):
                new_link = 'http://{}{}'.format(site_name, new_link)
            elif not re.search(r'https?://', new_link, re.IGNORECASE):
                new_link = 'http://{}'.format(new_link)

            if is_valid_url(new_link) and is_allowed_by_robots(disallow_list, new_link) and\
                            new_link not in already_parsed_pages:
                get_and_parse_whole_site(site_name, site_id, disallow_list, new_link, already_parsed_pages)


def download_html(pages):
    for page in pages:
        current_url = page[0]
        site_name = page[1]
        site_id = page[2]
        page_id = page[3]

        path_to_file = make_path_to_file(current_url, site_name)

        if re.search(r'[^\s]+robots\.txt$', current_url):
            if get_file(current_url, path_to_file):
                has_sitemap = parse_robots(path_to_file, site_id, mydb)
                if not has_sitemap[0]:
                    Logger.logger.info('Working with the site %s', site_name)
                    get_and_parse_whole_site(site_name, site_id, has_sitemap[1])
                    Logger.logger.info('The site %s has been parsed.', site_name)
        elif re.search(r'[S|s]itemap[^\s]*[\.xml]$', current_url):
            if get_file(current_url, path_to_file):
                parse_xml_sitemap(path_to_file, site_id, mydb)
        elif re.search(r'[S|s]itemap[^\s]*[\.gz]$', current_url):
            if get_file(current_url, path_to_file):
                if ungzip_file(path_to_file):
                    parse_xml_sitemap(path_to_file[:-3], site_id, mydb)
        elif re.search(r'[S|s]itemap[^\s]*[\.txt]$', current_url):
            if get_file(current_url, path_to_file):
                parse_txt_sitemap(path_to_file, site_id, mydb)
        else:
            if get_html_file(current_url, path_to_file):
                parse_html(path_to_file, site_id, page_id, mydb,
                           persons_dictionary, seek_words)

        mydb.set_pages_scantime(page_id)


def main():
    Logger.logger.info('Krauler started.')
    global persons_dictionary
    global seek_words

    persons_dictionary = mydb.get_persons
    seek_words = []

    for pair in persons_dictionary.items():
        seek_words.extend(pair[1])

    add_robots()

    new_pages = mydb.get_pages_without_scan
    download_html(new_pages)

    repeat_pages = mydb.get_pages_scanned_day_ago
    download_html(repeat_pages)

    Logger.logger.info('Krauler finished his work.')


if __name__ == '__main__':
    main()
