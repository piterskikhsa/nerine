#!/usr/bin/env python3.5
# coding: utf-8


from _datetime import datetime
import pymysql
import Logger


class NerineDb:
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
            except Exception:
                Logger.logger.error('Could not connect to the database.')
                exit(0)
            else:
                try:
                    result = func(self, cur, *args, **kwargs)
                except Exception as e2:
                    result = e2.args
                    conn.rollback()
                else:
                    conn.commit()
                finally:
                    cur.close()
                    conn.close()
            return result

        return decorated

    @property
    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    @property
    @mysql_connect
    def get_sites_without_pages(self, cur):
        sql = "SELECT id, Name FROM Sites WHERE Sites.id NOT IN(SELECT SiteID FROM Pages)"
        
        cur.execute(sql)
        result = cur.fetchall()

        return [result, sql]
    
    @property
    @mysql_connect
    def get_pages_without_scan(self, cur):
        sql = "SELECT Url, Name, SiteID, Pages.id FROM `Pages` INNER JOIN Sites on" \
              " Pages.Siteid = Sites.id WHERE Pages.LastScanDate IS NULL;"
        cur.execute(sql)
        result = cur.fetchall()

        return [result, sql]

    @property
    @mysql_connect
    def get_persons(self, cur):
        persons = {}
        try:
            sql = "SELECT Persons.id, Persons.Name, Keywords.Name AS Cname FROM Persons" \
                  " INNER JOIN Keywords ON Persons.id=Keywords.PersonID"
            cur.execute(sql)
        except Exception:
            Logger.logger.error('Could not get persons from the database.')
            return persons
        else:
            result = cur.fetchall()

        for row in result:
        # row[0] - Persons.id; row[1] - Persons.Name; row[2] - Keywords.Name related to exact person
            if row[0] not in persons:
                persons[row[0]] = [row[1], row[2]]
            else:
                persons[row[0]].append(row[2])
        return persons
    
    @mysql_connect
    def insert_pages_robots(self, cur, *args):
        url_robots = ''.join(['http://', args[0], '/robots.txt'])
        site_id = args[1]
        sql = "INSERT INTO `Pages` (Url, SiteID, FoundDateTime) VALUES (%s, %s, %s)"
        
        try:
            print('inserting robot', url_robots, site_id, self.get_time)
            cur.execute(sql, (url_robots, site_id, self.get_time))
        except Exception as error:
            print('kakaya-to xuinya', error)
            return [False, sql, args]
        else:
            return [True, sql, args]
    
    @mysql_connect
    def insert_pages_newone(self, cur, *args):
        # I would recode it to FoundDateTime='DEFAULT CURRENT_TIMESTAMP'
        # Only if we have mysql higher than 5.6.4
        sql = "INSERT INTO Pages(Url, SiteID, FoundDateTime) VALUES(%s,%s,%s)"
        try:
            cur.execute(sql, (args[0], args[1], self.get_time))
        except Exception:
            return [False, sql, args]
        else:
            return [True, sql, args]

    @mysql_connect
    def set_person_page_rank(self, cur, *args):
        # args=(PersonID, PageID, Rank)
        sql = "SELECT * FROM `PersonPageRank` WHERE `PageID`=%s"
        try:
            cur.execute(sql, (args[1],))
        except Exception:
            return [False, sql, args]
        else:
            already_in = cur.fetchall()

        if already_in:
            #print('the rank of person_id =', args[0], 'and page_id =', args[1], 'is already in the Database')
            sql = "UPDATE PersonPageRank SET Rank=%s WHERE PersonID=%s AND PageID=%s"
            params = (args[2], args[0], args[1])
        else:
            sql = "INSERT INTO PersonPageRank(PersonID, PageID, Rank) VALUES(%s,%s,%s)"
            params = args
            
        try:
            cur.execute(sql, params)
        except Exception as error:
            #print('error with adding page rank', error)
            return [False, sql, args]
        else:
            return [True, sql, params]
            
    @mysql_connect
    def set_pages_scantime(self, cur, *args):
        sql = "UPDATE `Pages` SET `LastScanDate`=%s WHERE id=%s"
        try:
            cur.execute(sql, (self.get_time, args[0]))
        except Exception as e:
            #print('error on lastscandate', e)
            return [False, sql, args]
        else:
            return [True, sql, args]
