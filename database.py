#!/usr/bin/env python
# !coding:utf-8
import pymysql
import uuid
import uuid


def connect_database(host, user, password, database, port):
    try:
        connect = pymysql.connect(host=host, user=user, password=password, db=database, port=port, charset='utf8')
        cursor = connect.cursor()
        return connect, cursor
    except Exception as e:
        print(e.args)


class DataBase(object):
    def __init__(self, host, user, password, database, port=3306):
        '''
        :param host:数据库IP地址
        :param user: 链接数据库用户名
        :param password: 链接数据库密码
        :param db: 需要链接的数据库
        :param port: 链接数据库端口
        '''
        self.host = host
        self.user = user
        self.passwd = password
        self.database = database
        self.port = port
        self.connect, self.cur = connect_database(self.host, self.user, self.passwd, self.database, self.port)

    def select_password_by_user_name_login(self, user_name):
        sql = '''select passwd,washingID from user where userID="%s"'''
        result = []
        try:
            self.cur.execute(sql % user_name)
            for i in self.cur.fetchall():
                result.extend([i[0], i[1]])
        except Exception as e:
            print(e.args)
        return result

    def update_user(self, user_name, washing_id):
        sql = '''update user set washingID=%d where userID="%s"'''
        try:
            self.cur.execute(sql % (washing_id, user_name))
            self.connect.commit()
            return True
        except Exception as e:
            print(e.args)
            return False

    def select_all_washing(self):
        result = []
        sql = '''select * from washing'''
        try:
            self.cur.execute(sql)
            for i in self.cur.fetchall():
                result.append([i[0], i[1], i[2], i[3]])
        except Exception as e:
            print(e.args)
        return result

    def update_washing_j(self, start_time, istrue, userID, washingID):
        sql = '''update washing set start_time=%d,istrue=%d,userID="%s" where washingID=%d'''
        try:
            self.cur.execute(sql % (start_time, istrue, userID, washingID))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    def update_washing_h(self, washingID):
        sql = '''update washing set start_time=%d,istrue=%d,userID="%s" where washingID=%d'''
        try:
            self.cur.execute(sql % (0, 0, " ", washingID))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)


if __name__ == '__main__':
    operating = DataBase("127.0.0.1", "root", "123", "test", 3306)
    print(operating.select_password_by_user_name_login("123"))
