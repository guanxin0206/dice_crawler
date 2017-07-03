#!/usr/bin/env python -t
# -*- coding: UTF-8 -*-
import urllib2
import requests


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None

        else:
            response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None

        return response.url, response.read()

    def download_json(self, url):
        if url is None:
            return None
        try:
            response = requests.get(url)
            d = response.json()
        except:
            raise
        return d
