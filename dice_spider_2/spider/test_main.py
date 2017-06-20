'''
Created on Jun 11, 2017

@author: xinguan
'''
import json_parser
import pprint

if __name__ == '__main__':
    url = ("http://service.dice.com/api/rest/jobsearch/" +
           "v1/simple.json?text=java&country=US&age=21&page=1")
    test_JsonParser_object = json_parser.JsonParser(url=url)
    d, nexturl, count = test_JsonParser_object.parse()
    # print nexturl
    # print count
    # pprint.pprint(d)
    print len(d.keys())
    pprint.pprint(d)
    # print len(d.keys())
