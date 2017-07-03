'''
Created on Jun 11, 2017

@author: xinguan
'''
# !/usr/bin/env python -t
# -*- coding: UTF-8 -*-
import mysql.connector


class MySQLInserter(object):

    def __init__(self, conn):
        self.conn = conn
        self.duplicate_counter = 0

    def insert(self, job_unique_id,
               job_title, job_url,
               company, post_date, job_description):
        cursor = self.conn.cursor()
        sql = ("INSERT INTO dice_jobs"
               "(job_unique_id, job_title, job_url, company"
               ", post_date, Job_description)"
               "VALUES ( %s,%s,%s,%s,%s,%s)")
        data = (job_unique_id, job_title, job_url,
                company, post_date, job_description)
        try:
            cursor.execute(sql, data)
            # print "last executed", cursor.last_executed_query()
            print "last statement:", cursor.statement
            if self.duplicate_counter != 0:
                self.duplicate_counter = 0
            self.conn.commit()

        except mysql.connector.IntegrityError as err:
            self.duplicate_counter += 1
            print "Error:{} ".format(err)
            self.conn.rollback()
            # raise Exception
        finally:
            cursor.close()
