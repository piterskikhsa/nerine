#!/usr/bin/env python
# coding: utf-8


import pymysql


class NerineDB:
    def __init__(self, host, port, user, passwd, db, charset):
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._db = db
        self._charset = charset
        
    def mysql_connect(func):
        def decorated(self, *args, **kwargs):
            try:
                conn = pymysql.connect(
                    host=self._host, port=self._port, user=self._user,
                    passwd=self._passwd, db=self._db, charset=self._charset)

                cur = conn.cursor()
            except Exception as e:
                result = e.args
            else:
                try:
                    result = func(self, cur, *args, **kwargs)
                except Exception as e2:
                    result = e2.args
                else:
                    conn.commit()
                finally:
                    cur.close()
                    conn.close()
            return result

        return decorated
        
    @property
    @mysql_connect
    def get_sites_without_pages(self, cur):
        sql = "SELECT ID FROM Sites WHERE Sites.ID NOT IN(SELECT SiteID FROM Pages)"
        
        cur.execute(sql)
        result = cur.fetchall()

        return result
    
    @property
    @mysql_connect
    def get_pages_without_scan(self, cur):
        sql = "SELECT Url,SiteID FROM Pages WHERE LastScanDate IS NULL"
        
        cur.execute(sql)
        result = cur.fetchall()

        return result
    
    @mysql_connect
    def insert_pages_robots(self, cur, *args):
        args[0] = ''.join([args[0],'/robots.txt'])
        sql = "INSERT INTO Pages(Url, SiteID) VALUES(%s,%s)"
        
        try:
            cur.execute(sql, args)
        except Exception:
            return [False, sql, args]
        else:
            return [True, sql, args]
    
    @mysql_connect
    def insert_pages_newone(self, cur, *args):
        # I would recode it to FoundDateTime='DEFAULT CURRENT_TIMESTAMP'
        # Only if we have mysql higher than 5.6.4
        sql = "INSERT INTO Pages(Url, SiteID, FoundDateTime) VALUES(%s,%s,%s)"
        
        try:
            cur.execute(sql, args)
        except Exception:
            return [False, sql, args]
        else:
            return [True, sql, args]
        
    @mysql_connect
    def set_person_page_rank(self, cur, *args):
        # args=[PersonID, PageID, Rank]
        sql = "SELECT * FROM `PersonPageRank` WHERE `PageID`=" + args[1]
        try:
            cur.execute(sql)
        except Exception:
            return [False, sql, args]
        else:
            already_in = cur.fetchall()
            
        # условие надо потестить, писал поток-сознанием, хотя тут все надо тестить
        if already_in:
            sql = "UPDATE PersonPageRank SET Rank=" + args[2] + "WHERE PageID=" + args[1]
        else:
            sql = "INSERT INTO PersonPageRank(PersonID, PageID, Rank) VALUES(%s,%s,%s)"
            
        try:
            cur.execute(sql, args)
        except Exception:
            return [False, sql, args]
        else:
            return [True, sql, args]
            
    @mysql_connect
    def set_pages_scantime(self, cur, *args):
        sql = "UPDATE `Pages` SET `LastScanDate`=" + args[1] + "WHERE PageID=" + args[0]
        try:
            cur.execute(sql, args)
        except Exception:
            return [False, sql, args]
        else:
            return [True, sql, args]
