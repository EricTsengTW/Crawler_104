#!/usr/bin/env python
# coding: utf-8

import pymysql


class MyConnect():
    def __init__(self):
        conn_cfg = {
            'host': '',
            'user': '',
            'password': '',
            'db': ''
        }
        self.conn = pymysql.connect(**conn_cfg)
        self.cursor = self.conn.cursor()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def queryone(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchone()

    # pure execute
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    # execute and commit
    def execmmit(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        self.conn.commit()

    def executemany(self, sql, params):
        self.cursor.executemany(sql, params)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
