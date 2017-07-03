'''
Created on Jun 14, 2017

@author: xinguan
'''
# import mysql.connector
import mysql.connector

create_dice_jobs = (
    "CREATE TABLE IF NOT EXISTS `dice_jobs` ("
    "  `job_unique_id` varchar(50) NOT NULL,"
    "  `job_title` text NOT NULL,"
    "  `job_url` text NOT NULL,"
    "  `company` text NOT NULL,"
    "  `post_date` date NOT NULL,"
    "  `job_description` text NOT NULL,"
    "  PRIMARY KEY (`job_unique_id`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='root', password='u6a3pwhe',
                              host='127.0.0.1',
                              database='dice_test')
cursor = cnx.cursor()
try:
    cursor.execute(create_dice_jobs)
    cnx.commit()
except mysql.connector.Error as err:
    print err
    cnx.rollback()
finally:
    cursor.close()
    cnx.close()
