#!/usr/bin/env python -t
# -*- coding: UTF-8 -*-
import requests


class JsonParser(object):

    def __init__(self, json_cont=None, url=None):
        if url is not None:
            self.url = url
            self.json_cont_dictionary = requests.get(url).json()

        self.json_cont_dictionary = json_cont

    def parse(self, json_cont_dict=None):
        if json_cont_dict is None:
            json_cont_dictionary = self.json_cont_dictionary
        else:
            json_cont_dictionary = json_cont_dict
        res_data = {}
        if 'nextUrl' in json_cont_dictionary.keys():
            nextUrl = json_cont_dictionary['nextUrl']
        else:
            nextUrl = None

        # keyword = "java"
        # count = json_cont_dictionary['count']

        resultItemList = json_cont_dictionary['resultItemList']

        for item in resultItemList:
            # jid is the job_unique id
            jid = item['detailUrl'].split('/')[6].split('?')[0].encode('utf-8')
            res_data[jid] = {}
            res_data[jid]['company'] = item['company'].encode('utf-8')
            res_data[jid]['date'] = item['date'].encode('utf-8')
            res_data[jid]['jobTitle'] = item['jobTitle'].encode('utf-8')
            res_data[jid]['location'] = item['location'].encode('utf-8')
            res_data[jid]['detailUrl'] = item['detailUrl'].encode('utf-8')

        return res_data, nextUrl
