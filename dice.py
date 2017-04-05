#!/usr/bin/env python -t
import requests, urllib, re, math, datetime, sys
from bs4 import BeautifulSoup
from init import *
import argparse
limit = 120
searchid = '9443532295942'
keyword_dict = {}

def getTotalCount(html1):
    '''On the First page, find total Count of jobs'''
    class1 = '#posiCountId'
    #print "class1 = ", class1
    for d1 in html1.select(class1):
        try:
            count_result = re.sub('.* of', '', d1.text).strip()
            count_result = re.sub('[^\d+]', '', count_result).strip()

            total_found = count_result

        except ValueError as ve:
            print "ValueError in getTotalCount:", ve
    return total_found


def getElementById(id,html1):
    for d2 in html1.select(id):
        #print d2.text
        try:
            element = d2.text.strip().encode('ascii', 'ignore').decode('ascii')
            element = re.sub('\'', '\\\'', element).strip()
        except ValueError:
            print "ValueError in getElementById", id
    #element = "random company"
    return element

def getDiceTitleById(id,html):
    tag = html.select(id)
    title = tag[0]['title'].strip().encode('ascii','ignore').decode('ascii')
    title = re.sub('\'','\\\'',title).strip()
    return title


def getPostDate(id,html1,i):
    element = html1.select(id)[i]
    try:
        element = element.text.strip().encode('ascii', 'ignore').decode('ascii')
        element = re.sub('\'', '\\\'', element).strip()
    except ValueError:
        print "ValueError in getPostDate", id
    return element

def getDiceURL(id,html1):
    element = html1.select(id)[0]
    url = element['href'].strip().encode('ascii', 'ignore').decode('ascii')
    return url

def getDiceJobDescription(url):
    try:
        response = requests.get(url)
    except Exception as e:
        print "Get Job Description Errors"
        print e
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

def count_job_keyword_in_db(keyword):

     nbre_element = 0

     qry = "SELECT COUNT(*) as nb FROM " + "dice_keywords" + " WHERE keyword='" + keyword +"'"
     print qry
     try:
         cursor.execute(qry)
         for row in cursor.fetchall():
             # print "execute(qry) = " , row
             nbre_element = re.sub('[^\d+]', '', str(row)).strip()
         connection.commit()
     except:
         connection.rollback()

     return int(nbre_element)


def check_element_in_TABLE1(element_name, element_value):

     element_exist = False

     qry = """ SELECT * FROM `""" + "dice_jobs" + """` WHERE `"""+ element_name +"""` LIKE '"""+ element_value +"""' """
     try:
         cursor.execute(qry)
         for row in cursor.fetchall():
             element_exist = True
             # print "execute(qry) = " , row
         connection.commit()
     except:
         connection.rollback()

     return element_exist

def convertStrDate(dateStr):

    date = datetime.datetime.now() - datetime.timedelta(0)
    date = date.strftime("%Y-%m-%d")

    try:
        if (re.search('Just|hour|minute|second|Today', dateStr)):
            try:
                date = datetime.datetime.now() - datetime.timedelta(0)
                date = date.strftime("%Y-%m-%d")
            except ValueError:
               ""
        else:
            try:
                dateStr2 = re.sub("\D", "", dateStr)
                dateStr2 = int(dateStr2)
                date = datetime.datetime.now() - datetime.timedelta(dateStr2)
                date = date.strftime("%Y-%m-%d")
            except ValueError as ve:
                print "ValueError:",ve
    except ValueError as ve:
        print "ValueError:",ve
    return date

def main():
  parser = argparse.ArgumentParser(description='Xin\'s dice.com crawler')
  parser.add_argument('-a','--all',action='store_true',dest='get_all',default=False,help='Get all jobs with all keywords in the input.txt')
  parser.add_argument('-n','--new',dest='get_all',action="store_false",help='Get only the new jobs with keywords in the input.txt file')
  parser.add_argument('-k','--keywords',dest='keywords',nargs="+",help="Take only one keyword to fetch that particular keyword")
  args = parser.parse_args()
  print (args.get_all, args.keywords)
  if args.keywords != None:
    keywords = args.keywords

  if args.get_all:
      print "get_all:",args.get_all
  else:
    print "get_all:",args.get_all

  with open(input_keyword_file) as f:
    for line in f:    # Corner case not empty line

      dup_count = 0
      break_for = False
      fetched_count = 0

      keyword = line
      keyword = keyword.strip()
      print "keyword:%s" %keyword
      keyword_dict[keyword] = (0,0)

      """if(count_job_keyword_in_db(keyword) == 0):"""
      print "========================================"
      print 'get all data'
      print "========================================"

      #url = 'https://www.dice.com/jobs?q=' + urllib.quote_plus(keyword) +'&limit='+str(limit)+'&sort=date&l=&searchid='+searchid
      url = 'https://www.dice.com/jobs?q=' + urllib.quote_plus(keyword) +'&limit='+str(limit)+'&l=&searchid='+searchid
      req = requests.get(url)
      req.raise_for_status()
      if req != None:
        html1 = BeautifulSoup(req.content, "html5lib")
      else:
        raise

      total_found = getTotalCount(html1)
      count_result = total_found
      print "Total Found", total_found

      count_page = math.ceil(int(count_result)/limit)
      rest_count_page = int(count_result)%limit
      if(rest_count_page > 0):
          count_page = count_page + 1

      count_page = int(count_page)
      print "count_page:", count_page

      for i in range(1,count_page+1):   #Page Navigation
        if i == 1:
          try:
            req = requests.get(url)
            print "Sucess fetching Page:", i
            print "Remaining page:%i, Total page:%i" %(count_page-i, count_page)
            

          except requests.RequestException as err:
              print "Requests Error:", err
          print req.url

          if req.content != None:
              try:
                  html1 = BeautifulSoup(req.content, "html5lib")
              except Exception as err2:
                  print err2
          else:
              raise 
          for i in range(0,limit):
            #print req.url
            class1 = '#company'+str(i)
            print class1
            company = getElementById(class1,html1)

            class1 = '#position'+str(i)
            try:
              job_title = getDiceTitleById(class1,html1)
              job_url = getDiceURL(class1,html1)

              dice_id = job_url.split('/')[7].split('?')[0]

              job_description = getDiceJobDescription(job_url)
              #job_description = "test blah blah"
              class1 = '.posted'
              post_date = getPostDate(class1,html1,i)
              post_date = convertStrDate(post_date)
            except:
              continue

            element_exist = check_element_in_TABLE1("job_unique_id", dice_id)

            if(element_exist==False):
                #write 120 entries into it
                insert_Into_Table2(keyword,job_title,job_url,company,post_date,dice_id,job_description)
                fetched_count = fetched_count + 1
                dup_count = 0
            else:
              pass       
        elif(i==count_page):
          try:
              req = requests.get('https://www.dice.com/jobs?q='+urllib.quote_plus(keyword)+'&startPage='+str(i)+'&limit='+str(limit)+'&l=&searchid='+searchid)
              #req = requests.get('https://www.dice.com/jobs/q-program_analyst-limit-'+str(limit)+'-startPage-'+str(i)+'-limit-'+str(limit)+'-jobs?searchid='+searchid)
              print "Sucess for %i" %i
              print "Remaining page:%i, Total page:%i" %(count_page-i, count_page)
          except requests.RequestException as err:
              print "Requests Error:", err
              req.raise_for_status()

          print req.url
          if req.content != None:
              try:
                  html1 = BeautifulSoup(req.content, "html5lib")
              except Exception as err2:
                  print err2
          else:
              raise 
          for i in range(0,rest_count_page):
              #print req.url
              class1 = '#company'+str(i)
              print class1
              try:
                company = getElementById(class1,html1)
                class1 = '#position'+str(i)
                job_title = getDiceTitleById(class1,html1)
                job_url = getDiceURL(class1,html1)
                dice_id = job_url.split('/')[7].split('?')[0]
                job_description = getDiceJobDescription(job_url)
                #job_description = "test blah blah"
                class1 = '.posted'
                post_date = getPostDate(class1,html1,i)
                post_date = convertStrDate(post_date)
              except:
                continue
              element_exist = check_element_in_TABLE1("job_unique_id", dice_id)

              if(element_exist==False):
                  #write 120 entries into it
                  insert_Into_Table2(keyword,job_title,job_url,company,post_date,dice_id,job_description)
                  #print "Inserted %i entries, %s" %(i,job_title)
                  fetched_count = fetched_count + 1
                  dup_count = 0
              else:
                pass
        else:
          try:
              req = requests.get('https://www.dice.com/jobs?q='+urllib.quote_plus(keyword)+'&startPage='+str(i)+'&limit='+str(limit)+'&l=&searchid='+searchid)
              #req = requests.get('https://www.dice.com/jobs/q-program_analyst-limit-'+str(limit)+'-startPage-'+str(i)+'-limit-'+str(limit)+'-jobs?searchid='+searchid)
              print "Sucess for %i" %i
          except requests.RequestException as err:
              print "Requests Error:", err
              req.raise_for_status()

          print req.url

          if req.content != None:
              try:
                  html1 = BeautifulSoup(req.content, "html5lib")
              except Exception as err2:
                  print err2
          else:
              raise 
              
          for i in range(0,limit):
            #print req.url
            class1 = '#company'+str(i)
            print class1
            company = getElementById(class1,html1)

            class1 = '#position'+str(i)
            try:
              job_title = getDiceTitleById(class1,html1)
              job_url = getDiceURL(class1,html1)
              dice_id = job_url.split('/')[7].split('?')[0]
              job_description = getDiceJobDescription(job_url)
              #job_description = "test blah blah"
              class1 = '.posted'
              post_date = getPostDate(class1,html1,i)
              post_date = convertStrDate(post_date)
            except:
              continue
            element_exist = check_element_in_TABLE1("job_unique_id", dice_id)

            if(element_exist==False):
                #write 120 entries into it
                insert_Into_Table2(keyword,job_title,job_url,company,post_date,dice_id,job_description)
                #print "Inserted %ith entries, %s" %(i,job_title)
                fetched_count = fetched_count + 1
                dup_count = 0
            else:
              pass
        keyword_dict[keyword] = (total_found, fetched_count) 
      """
      else:
        print "========================================"
        print 'get filtered data'
        print "========================================"

        url = 'https://www.dice.com/jobs?q=' + urllib.quote_plus(keyword) +'&limit='+str(limit)+'&l=&searchid='+searchid
        req = requests.get(url)
        req.raise_for_status()
        if req != None:
          html1 = BeautifulSoup(req.content, "html5lib")
        else:
          raise

        total_found = getTotalCount(html1)
        count_result = total_found
        print "Total Found", total_found

        count_page = math.ceil(int(count_result)/limit)
        rest_count_page = int(count_result)%limit
        if(rest_count_page > 0):
            count_page = count_page + 1

        count_page = int(count_page)
        print "count_page:", count_page

        for i in range(1,count_page+1):   #Page Navigation
          try:
              req = requests.get('https://www.dice.com/jobs?q='+urllib.quote_plus(keyword)+'&startPage='+str(i)+'&limit='+str(limit)+'&l=&searchid='+searchid)
              #req = requests.get('https://www.dice.com/jobs/q-program_analyst-limit-'+str(limit)+'-startPage-'+str(i)+'-limit-'+str(limit)+'-jobs?searchid='+searchid)
              print "Sucess for %i" %i
          except requests.RequestException as err:
              print "Requests Error:", err
              req.raise_for_status()

          print req.url

          if req.content != None:
              try:
                  html1 = BeautifulSoup(req.content, "html5lib")
              except Exception as err2:
                  print err2
          else:
              raise 


          for i in range(0,limit):
            #print req.url
            class1 = '#company'+str(i)
            print class1
            try:
              company = getElementById(class1,html1)
              class1 = '#position'+str(i)
              job_title = getDiceTitleById(class1,html1)
              job_url = getDiceURL(class1,html1)
              dice_id = job_url.split('/')[7].split('?')[0]
              job_description = getDiceJobDescription(job_url)
              class1 = '.posted'
              post_date = getPostDate(class1,html1,i)
              post_date = convertStrDate(post_date)
            except:
              continue

            element_exist = check_element_in_TABLE1("job_unique_id", dice_id)

            if(element_exist==False):
                #write 120 entries into it
                insert_Into_Table2(keyword,job_title,job_url,company,post_date,dice_id,job_description)
                #print "Inserted %i entries, %s" %(i,job_title)
                fetched_count = fetched_count + 1
                dup_count = 0
            else:
                print  "Found duplicate in data base at %i, %s"%(i,job_title)
                dup_count += 1  #consecute 5 dup_count
                if dup_count > 5:
                    break_for = True
                    print '################found duplicate###################'
                    break
          
          if(break_for == True):
              print '################found duplicate###################'
              break 
          keyword_dict[keyword] = (total_found, fetched_count) 
        """
  print keyword_dict

if __name__ == "__main__": 
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt"
		sys.exit(0)
