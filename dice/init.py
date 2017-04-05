#!/usr/bin/env python
import requests,urllib,re,math,MySQLdb
from bs4 import BeautifulSoup


################################ START configuration ########################
useProxy = True
input_keyword_file = 'input.txt'
input_proxy_file = 'proxy.txt'
proxy_username = 'US219524'
proxy_password = 'EhYksL7ttc'
################################ START configuration ########################

################################ START database configuration ########################
host = 'localhost'
user = 'root'
password = 'u6a3pwhe'
dataBaseName = 'mentorx_test'
#DB_tableName1 = 'indeed_jobs'
################################ END database configuration ########################

################################ START CREATE DATABASE #############################
connection = MySQLdb.connect(host, user, password)
cursor = connection.cursor()
sql = 'CREATE DATABASE IF NOT EXISTS `'+ dataBaseName +'` CHARACTER SET utf8 COLLATE utf8_general_ci;'
cursor.execute(sql)
cursor.close()
################################ END CREATE DATABASE ###############################

################################ START connection to Mysql #########################
connection = MySQLdb.connect(host, user, password, dataBaseName)
cursor = connection.cursor()
################################ END connection to Mysql ##########################

################################ START CREATE TABLE ##############################
qry = """
  CREATE TABLE IF NOT EXISTS dice_jobs (
  
  job_unique_id VARCHAR(50) NOT NULL,
  job_title text NOT NULL,
  job_url text NOT NULL,
  company text NOT NULL,
  post_date date NOT NULL,
  job_description text NOT NULL,
  PRIMARY KEY (job_unique_id )) ENGINE = MYISAM DEFAULT CHARSET=utf8;
  """
try:
    cursor = connection.cursor( MySQLdb.cursors.DictCursor )
    cursor.execute(qry)
except:
    connection.rollback()

qry = """
  CREATE TABLE IF NOT EXISTS dice_keywords (
    keyword text NOT NULL,
    job_unique_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (job_unique_id) REFERENCES dice_jobs(job_unique_id)
    ) ENGINE = MYISAM DEFAULT CHARSET=utf8;
  """
try:
    cursor = connection.cursor( MySQLdb.cursors.DictCursor )
    cursor.execute(qry)
except:
    connection.rollback()
################################ END CREATE TABLE ##############################
