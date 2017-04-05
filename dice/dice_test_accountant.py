#!/usr/bin/env python
import requests, urllib, re, math
from bs4 import BeautifulSoup
from indeed import convertStrDate
from config import *
import pickle,json,sys,os

input_keyword_file = "input2.txt"

def get_url(keyword,startpage=1,sortby="date",limit=120,searchid=1538219000213):
  if startpage==1:
    url = 'https://www.dice.com/jobs?q=' + urllib.quote_plus(keyword) +'&limit='+str(limit)+'&l=&searchid='+str(searchid) + '&sort=' +sortby
  else:
    url = 'https://www.dice.com/jobs?q='+urllib.quote_plus(keyword)+'&startPage='+str(startpage)+'&limit='+str(limit)+'&l=&searchid='+ str(searchid) + '&sort=' +sortby
  return url

def getCountPage(count_result,limit):
  """This function returns the total number count pages of """
  count_page = math.ceil(int(count_result)/limit)
  rest_count_page = int(count_result)%limit
  if(rest_count_page > 0):
      count_page = count_page + 1
  count_page = int(count_page)

  return (count_page,rest_count_page)

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
  print "Total Found:",total_found
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

def main():
  searchid = '9443532295942'
  limit = 120
  dup_count = 0
  keyword_dict = {}
  break_for = False
  fetched_count = 0

  my_set = set()
  my_set2 = set()
  output = open('my_set_relevance.pkl', 'wb')
  with open(input_keyword_file) as f:
    for keyword in f:
      print "========================================"
      print 'get all data'
      print "========================================"
      keyword = keyword.strip()
      keyword = keyword.strip("\n")
      #keyword_dict[keyword] = (0,0)
      print "keyword:%s"%keyword
      
      url1 = get_url(keyword,sortby="relevance"); url2 = get_url(keyword,sortby="date")

      req = requests.get(url1)
      req.raise_for_status()
      if req != None:
        html1 = BeautifulSoup(req.content, "html5lib")
      else:
        raise

      print "url:",url1
      count_result = getTotalCount(html1)
      count_page,rest_count_page = getCountPage(count_result,limit)
      print "count_page:", count_page

      keyword_dict[keyword+'_relevance'] = (count_result, fetched_count)  

      req = requests.get(url2)
      req.raise_for_status()
      if req != None:
        html1 = BeautifulSoup(req.content, "html5lib")
      else:
        raise

      print "url:",url2
      count_result = getTotalCount(html1)

      count_page,rest_count_page = getCountPage(count_result,limit)
      print "count_page:", count_page

      keyword_dict[keyword+'_date'] = (count_result, fetched_count)  
      
      if(keyword_dict[keyword +'_relevance'][0]!=keyword_dict[keyword+'_date'][0]):
      
        for i in range(1,count_page + 1):   #Page Navigation
          if i == 1:
            #continue
            try:
              req = requests.get(url1)
              print "Sucessfully fetching Page:",i
              print "Remaining page:%i, Total page:%i" %(count_page-i, count_page)
              print req.url

            except requests.RequestException as err:
              print "Requests Error:", err

            for i in range(0,limit):
              #print req.url
              class1 = '#company'+str(i)
              print class1
              company = getElementById(class1,html1)

              class1 = '#position'+str(i)
              job_title = getDiceTitleById(class1,html1)
              job_url = getDiceURL(class1,html1)

              dice_id = job_url.split('/')[7].split('?')[0]
              job_unique_id = dice_id

              job_description = getDiceJobDescription(job_url)
              #job_description = "test blah blah"
              class1 = '.posted'
              post_date = getPostDate(class1,html1,i)
              post_date = convertStrDate(post_date)

              #element_exist = check_element_in_TABLE1("job_unique_id", dice_id)
              element_exist = job_unique_id in my_set

              if(element_exist==False):
                  #write 120 entries into it
                  #insert_Into_Table2(keyword,job_title,job_url,company,post_date,dice_id,job_description)
                  try:
                    my_set.add(job_unique_id)
                    print "Added %ith entries, %s into the set" %(i,job_title)
                  except:
                    print "problems with adding dice_id into a set"
                  fetched_count = fetched_count + 1
                  dup_count = 0
              else:
                pass  
        
          elif(i == count_page):  #last page
            url1 = get_url(keyword,i,'relevance')
            try:

                req = requests.get(url1)
                
                print "Sucessfully fetching page %i, the last page" %i
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
                company = getElementById(class1,html1)

                class1 = '#position'+str(i)
                job_title = getDiceTitleById(class1,html1)
                job_url = getDiceURL(class1,html1)

                dice_id = job_url.split('/')[7].split('?')[0]
                job_unique_id = dice_id

                job_description = getDiceJobDescription(job_url)
                #job_description = "test blah blah"
                class1 = '.posted'
                post_date = getPostDate(class1,html1,i)
                post_date = convertStrDate(post_date)

                #element_exist = check_element_in_TABLE1("job_unique_id", dice_id)
                element_exist = job_unique_id in my_set

                if(element_exist==False):
                  #write 120 entries into it
                  #insert_Into_Table2(keyword,job_title,job_url,company,post_date,dice_id,job_description)
                  my_set.add(job_unique_id)
                  print "Added %i entries, %s into the set" %(i,job_title)
                  fetched_count = fetched_count + 1
                  dup_count = 0
                else:
                  pass 
        
          else:
            # continue
            try:
              req = requests.get(get_url(keyword,i,'relevance'))
              #req = requests.get('https://www.dice.com/jobs/q-program_analyst-limit-'+str(limit)+'-startPage-'+str(i)+'-limit-'+str(limit)+'-jobs?searchid='+searchid)
              print "Sucessfully fetching Page:",i
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

            for i in range(0,limit):
              #print req.url
              class1 = '#company'+str(i)
              print class1
              company = getElementById(class1,html1)

              class1 = '#position'+str(i)
              job_title = getDiceTitleById(class1,html1)
              job_url = getDiceURL(class1,html1)

              dice_id = job_url.split('/')[7].split('?')[0]
              job_unique_id = dice_id

              job_description = getDiceJobDescription(job_url)
              #job_description = "test blah blah"
              class1 = '.posted'
              post_date = getPostDate(class1,html1,i)
              post_date = convertStrDate(post_date)

              #element_exist = check_element_in_TABLE1("job_unique_id", dice_id)
              element_exist = job_unique_id in my_set

              if(element_exist==False):
                  #write 120 entries into it
                  #insert_Into_Table2(keyword,job_title,job_url,company,post_date,dice_id,job_description)
                  my_set.add(job_unique_id)
                  print "Added %ith entries, %s into the set" %(i,job_title)
                  fetched_count = fetched_count + 1
                  dup_count = 0
              else:
                pass
        break
    # Pickle the list using the highest protocol available.
    pickle.dump(my_set, output, -1)
    output.close()
      #keyword_dict[keyword] = (total_found,f)

    print keyword_dict  
    # with open('my_file.json','w') as f:
    # data = keyword_dict
    # json.dump(data, f)
    
    print "Set length:",len(my_set)

if __name__ == "__main__": 
  try:
    main()
  except KeyboardInterrupt:
      print 'Interrupted'
      try:
          sys.exit(0)
      except SystemExit:
          os._exit(0)