#!/usr/bin/env python -tt
# -*- coding: iso-8859-15 -*-
import requests,urllib,re,math,datetime,sys
from bs4 import BeautifulSoup
import argparse

input_keyword_file = "input.txt"

#with open(input_keyword_file) as f:
#试试中文

def main():
  parser = argparse.ArgumentParser(description='Xin\'s dice.com crawler')
  parser.add_argument('-a','--all',action='store_true',dest='get_all',default=False,help='Get all jobs with all keywords in the input.txt')
  parser.add_argument('-n','--new',dest='get_all',action="store_false",help='Get only the new jobs with keywords in the input.txt file')
  #parser.add_argument("-v","--verbose",dest=verbosity)
  parser.add_argument('-k','--keyword',dest='keyword',nargs="+",help="Take only one keyword to fetch that particular keyword")
  args = parser.parse_args()
  #print type(parser)
  #args.get_all
  print (args.get_all, args.keyword)
  if args.keyword != None:

    print "keywords:",args.keyword
  if args.get_all:
    print "get_all:",args.get_all
  else:
    print "get_all:",args.get_all

if __name__ == "__main__":
  main()
