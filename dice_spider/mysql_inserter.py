#!/usr/bin/env python -t
# -*- coding: UTF-8 -*-

class MySQLInserter(object):
  def __init__(self):
    self.qry = 

  def insert(self):
    pass
    
  def __insert_new_data(self):
    pass

  def __insert_new_url(self):
    pass


################################ START database configuration ########################
host = 'localhost'
user = 'root'
password = 'u6a3pwhe'
dataBaseName = 'dice_test'
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
qry2 = """
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
else:
  connection.commit()

try:
    cursor = connection.cursor( MySQLdb.cursors.DictCursor )
    cursor.execute(qry2)
except:
    connection.rollback()
else:
  connection.commit()
################################ END CREATE TABLE ##############################

def insert_Into_Table(keyword,job_title,job_url,company,post_date,job_unique_id,Job_description):
    qry = """
      INSERT INTO dice_jobs(job_unique_id, job_title, job_url, company, post_date, Job_description)
      VALUES ( %s,%s,%s,%s,%s,%s);
    """

    qry2 = """
      INSERT INTO dice_keywords(keyword,job_unique_id)
      VALUES (%s,%s);
    """
    try:
        cursor.execute(qry,(job_unique_id,job_title,job_url,company,post_date,Job_description))
        print "Inserted succesful Query1, %s, %s" %(job_title,job_unique_id)
    except (KeyboardInterrupt, SystemExit):
       connection.rollback()
       raise
    except Exception as e:
        connection.rollback()
        print "INSERTION ERROR!"
        print qry
        print e
        #raise
    else:
        connection.commit()
    try:
      cursor.execute(qry2,(keyword,job_unique_id))
      print "Inserted succesful Query2, %s, %s" %(job_title,job_unique_id)
    except (KeyboardInterrupt, SystemExit):
      connection.rollback()
      raise
    except Exception as e:
      connection.rollback()
      print "INSERTION ERROR!"
      print qry2
      raise
    else:
      connection.commit()