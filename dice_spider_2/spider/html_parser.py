#!/usr/bin/env python -t
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import re
import urlparse


class HtmlParser(object):

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self.__get_new_data(page_url, soup)
        job_description = new_data
        return job_description

    def __get_new_urls(self, page_url, soup):
        new_urls = set()
        # /item/Python.htm
        # ?
        links = soup.find_all('a', href=re.compile(r"/item/*"))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def __get_new_data(self, page_url, soup):
        # <div class="highlight-black" id="jobdescSec">
        try:
            jd_node = soup.find(id="jobdescSec").get_text()
        except AttributeError:
            print "404 page no longer exists", page_url
            return None
        except Exception as err:
            print "other errors while parsing web page", err
        return jd_node
