'''
Created on Jun 12, 2017

@author: xinguan
'''
import mysql_inserter
import mysql.connector
 
################################ START database configuration ########################
host = 'localhost'
user = 'root'
password = 'u6a3pwhe'
db = 'dice_test'

conn = mysql.connector.connect(user=user, password=password, database=db)
inserter = mysql_inserter.MySQLInserter(conn)
job_unique_id = "test"
job_title = "test"
job_url = "test"
company = "test"
post_date = "2017-06-12"
job_description = "test"
try:
    inserter.insert(job_unique_id, job_title, job_url, company, post_date, job_description)
except:
    raise
finally:
    conn.close()