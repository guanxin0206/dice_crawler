import requests,re,math,MySQLdb
from bs4 import BeautifulSoup
from config import *
from indeed import *

################################ START CREATE DATABASE #############################
connection = MySQLdb.connect(mysql['host'], mysql['user'], mysql['password'])
cursor = connection.cursor()
sql = 'CREATE DATABASE IF NOT EXISTS `'+ mysql['dataBaseName'] +'` CHARACTER SET utf8 COLLATE utf8_general_ci;'
cursor.execute(sql)
cursor.close()
################################ END CREATE DATABASE ###############################

################################ START connection to Mysql #########################
connection = MySQLdb.connect(mysql['host'], mysql['user'], mysql['password'], mysql['dataBaseName'])
cursor = connection.cursor()
################################ END connection to Mysql ##########################

################################ START CREATE TABLE ##############################
qry = """
    CREATE TABLE IF NOT EXISTS """+mysql['DB_tableName1']+""" (
	id INT NOT NULL AUTO_INCREMENT,

    keyword text NOT NULL,
    job_title text NOT NULL,
    job_url text NOT NULL,
    company text NOT NULL,
    post_date date NOT NULL,
    job_unique_id text NOT NULL,
    Job_description text NOT NULL,

	PRIMARY KEY (id) ) ENGINE = MYISAM DEFAULT CHARSET=utf8 ;
    """
qry2 = """
    
    """

try:
    cursor = connection.cursor( MySQLdb.cursors.DictCursor )
    cursor.execute(qry)
except:
    connection.rollback()
################################ END CREATE TABLE ##############################

################################ START AUX FUNCTION ##############################

def getElementById(id,html1):
    #class2 = dice[id]
    for d2 in html1.select(id):
        try:
            element = d2.text.strip().encode('ascii', 'ignore').decode('ascii')
            element = re.sub('\'', '\\\'', element).strip()
        except ValueError:
            print "ValueError on", id
    return element

def getPostDate(id,html1,i):
    element = html1.select(id)[i]
    try:
        element = element.text.strip().encode('ascii', 'ignore').decode('ascii')
        element = re.sub('\'', '\\\'', element).strip()
    except ValueError:
        print "ValueError on", id
    return element

def getDiceURL(id,html1):
    element = html1.select(id)[0]
    url = element['href'].strip().encode('ascii', 'ignore').decode('ascii')
    return url

def getDiceJobDescription(url):
    try:
        response = requests.get(url)
    except:
        ""
    html = BeautifulSoup(response.content,"html5lib")
    id = "#jobdescSec"
    description = html.select(id)
    text = ""
    for tag in description:
        tag = tag.text.strip().encode('ascii', 'ignore').decode('ascii')
        tag = re.sub('\'', '\\\'', tag).strip()
        text = text + tag
    #text = text.strip()
    return text
    
def insert_Into_Table2(keyword,job_title,job_url,company,post_date,job_unique_id,Job_description):

    qry = """
    INSERT INTO `""" + mysql['DB_tableName1'] + """` (`id`, `keyword`, `job_title`, `job_url`, `company`, `post_date`, `job_unique_id`, `Job_description`)
    VALUES (NULL,
    '""" + keyword + """',
    '""" + job_title + """',
    '""" + job_url + """',
    '""" + company + """',
    '""" + post_date + """',
    '""" + job_unique_id + """',
    '""" + Job_description + """');
    """

    try:
        cursor.execute(qry)
        connection.commit()
    except:
        connection.rollback()

################################ START MAIN FUNCTION ##############################

def main():

    keyword_dict = {}

    f = open(input_keyword_file)
    for keywords in f.readlines():
        keyword = ''
        keyword = keywords.strip()
        print 'keyword = ', keyword
        keyword_dict[keyword] = (0,0)

        dup_count = 0
        total_found = 0
        fetched_count = 0

        print "========================================"
        print 'get filtered data'
        print "========================================"
        
        str1 = requests.get('https://www.dice.com/jobs?q=' + urllib.quote_plus(keyword) +'&limit=50&l=&searchid=9443532295942')

        str1.raise_for_status()

        html1 = BeautifulSoup(str1.content, "html5lib")

        for i in range(0,50):
            
            class1 = '#company'+str(i)
            company = getElementById(class1,html1)

            class1 = '#position'+str(i)
            job_title = getElementById(class1,html1)
            job_url = getDiceURL(class1,html1)

            dice_id = job_url.split('/')[7].split('?')[0]

            job_description = getDiceJobDescription(job_url)
            #job_description = "test blah blah"
            class1 = '.posted'
            post_date = getPostDate(class1,html1,i)
            post_date = convertStrDate(post_date)

            
            #write 50 entries into it
            insert_Into_Table2(keyword,job_title,job_url,company,post_date,dice_id,job_description)
            fetched_count = fetched_count + 1

        '''One perpage total Count of jobs'''
        class1 = '#posiCountId'
        #print "class1 = ", class1
        for d1 in html1.select(class1):
            try:
                count_result = re.sub('.* of', '', d1.text).strip()
                count_result = re.sub('[^\d+]', '', count_result).strip()

                total_found = count_result

                count_page = math.ceil(int(count_result)/50)
                rest_count_page = int(count_result)%50
                if(rest_count_page > 0):
                    count_page = count_page + 1

                if(count_page>20):
                    count_page = 20

            except ValueError as ve:
                print "ValueError:", ve

        total_found = count_result
        print 'count_result = ', count_result
        # print 'company:', company
        # print 'title:', title
        # print 'post_date:', post_date
        # print 'url:' , url
        # print 'dice_id:',dice_id
        # print 'description:',job_description
        keyword_dict[keyword] = (total_found, fetched_count)
        print keyword_dict

if __name__ == "__main__": main()

