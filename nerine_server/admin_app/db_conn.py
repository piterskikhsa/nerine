import pymysql


class DBConnection:
    def __init__(self, host, user, password, db, charset):
        self._host = host
        self._user = user
        self._password = password
        self._db = db
        self._charset = charset
        self._cur = self.connetct_to_base()
        self._result = []

    def connetct_to_base(self):
        conn = pymysql.connect(host=self._host,
                               user=self._user,
                               passwd=self._password,
                               db=self._db,
                               charset=self._charset)
        cur = conn.cursor()
        return cur

    def rework_list(self, ls):
        for item in ls:
            self._result.append(item[0])
        return self._result

    def get_list_sites(self):
        sql = "SELECT Name FROM nerine_db.Sites;"
        self._cur.execute(sql)
        data_list = self._cur.fetchall()
        sites_list = self.rework_list(data_list)
        return sites_list

    def get_list_persons(self):
        sql = "SELECT Name FROM nerine_db.Persons;"
        self._cur.execute(sql)
        data_list = self._cur.fetchall()
        persons_list = self.rework_list(data_list)
        return persons_list

    def get_list_keywords(self):
        sql = "SELECT Name FROM nerine_db.Keywords;"
        self._cur.execute(sql)
        data_list = self._cur.fetchall()
        keywords_list = self.rework_list(data_list)
        return keywords_list




# data = DBConnection('localhost', 'newuser', 'password', 'nerine_db', 'utf8mb4')
# persons = data.get_list_persons()
# print(persons)
