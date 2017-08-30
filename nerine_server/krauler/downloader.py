#!/usr/bin/env python
# coding: utf-8


import re
import urllib.request
import gzip
from config import db_host, db_port, db_username, db_password, db_name, db_charset
import NerineDB
import  Logger
from Parser import parse_robots, parse_xml_sitemap, parse_html, make_path_to_file,\
    parse_url, parse_txt_sitemap


mydb = NerineDB.NerineDb(
        db_host , db_port, db_username, db_password, db_name, db_charset)


def add_robots():
    new_sites = mydb.get_sites_without_pages
    for i in new_sites[0]:
        r = mydb.insert_pages_robots(i[1], i[0])
        if r[0]:
            Logger.logger.info('new robots page inserted.')
            #print('new robots page inserted.')
        else:
            #print(r[0])
            Logger.logger.error('could not insert robots.txt for %s', i[1])


def get_file(url, file):
    try:
        Logger.logger.info('getting a file... %s', url)
        urllib.request.urlretrieve(url, file)
    except Exception as error:
        #print(error)
        Logger.logger.error('could not get: %s. output: %s', url, error)
        return False
    else:
        #print('got', url)
        Logger.logger.info('GOT: %s. PUT it to %s', url, file)
        return True


def get_html_file(url, file_path):
    #print('getting NOT parsed url..', url)
    #print('file path is', file_path)
    Logger.logger.info('getting a html file %s:', url)
    if '?' and '=' in url:
        url = parse_url(url)
    try:
        Logger.logger.info('found http GET request. parsing params..')
        req = urllib.request.urlopen(url)
    except Exception as error:
        #print(error)
        Logger.logger.error('could not get %s: output:', url, error)
        return False
    else:
        try:
            Logger.logger.info('checking content-type..')
            content_type = req.info().get_content_subtype()
        except Exception as error:
            #print(error)
            Logger.logger.error('could not get %s', url)
            return False
        else:
            if re.search(r'[html|HTML]', content_type):
                try:
                    charset = req.info().get_content_charset()
                except Exception as error:
                    #print(error)
                    Logger.logger.error('could not determine charset. %s . going to use utf-8..', error)
                    content = req.read().decode('utf-8')
                else:
                    content = req.read().decode(charset)
                    #print('charset =', charset)
                    Logger.logger.info('charset is %s', charset)
                finally:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    #print('got', url)
                    Logger.logger.info('GOT %s', url)

                return True
            else:
                #print(url, 'bad content-type:', content_type)
                Logger.logger.error('%s has a bad content-type: %s', url, content_type)
                return False


def ungzip_file(gz_file):
        out_xml_file = gz_file[:-3]

        try:
            with gzip.open(gz_file, 'rb') as f:
                content = f.read()
        except Exception as error:
            #print(error)
            Logger.logger.error('could not decompress %s . output: %s', gz_file, error)
            return False
        else:
            try:
                with open(out_xml_file, 'wb') as f2:
                    f2.write(content)
            except Exception as error:
                #print(error)
                Logger.logger.info('could not open %s . output: %s', out_xml_file, error)
            else:
                #print(gz_file, 'was successfully ungzipped.')
                Logger.logger.info('%s was succesfully decompressed.', gz_file)
                return True


def download_html():
    new_pages =  mydb.get_pages_without_scan

    for url in new_pages[0]:
        current_url = url[0]
        site_name = url[1]
        site_id = url[2]
        page_id = url[3]

        path_to_file = make_path_to_file(current_url, site_name)
        #print('path to file in downloader', path_to_file)

        if re.search(r'[^\s]+robots\.txt$', current_url):
            if get_file(current_url, path_to_file):
                parse_robots(path_to_file, site_id, mydb)
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
