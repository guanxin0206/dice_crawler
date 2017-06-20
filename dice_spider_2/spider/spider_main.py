#!/usr/bin/env python -t
# -*- coding: UTF-8 -*-
import url_manager
import html_parser
import html_outputer
import html_downloader
import mysql_inserter
import json_parser
import mysql.connector


class SpiderMain(object):

    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.html_parser = html_parser.HtmlParser()
        self.json_parser = json_parser.JsonParser()
        self.outputer = html_outputer.HtmlOutputer()
        conn = mysql.connector.connect(user='root', password='u6a3pwhe',
                                       database='dice_test')
        self.inserter = mysql_inserter.MySQLInserter(conn)

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url() or count <= 10:
            try:
                new_url = self.urls.get_new_url()
                print "Craw %d : %s" % (count, new_url)
                json_cont = self.downloader.download_json(new_url)

                data_dict, next_url = self.json_parser.parse(json_cont)

                for key in data_dict:
                    # TODO: html_downloader returns url, html_cont
                    real_url, html_cont = self.downloader.download(
                                        data_dict[key]['detailUrl'])
                    data_dict[key]['detailUrl'] = real_url
                    job_description = self.html_parser.parse(real_url,
                                                             html_cont)
                    data_dict[key]['jobDescription'] = job_description
                    self.inserter.insert(key, data_dict[key]['jobTitle'],
                                         data_dict[key]['detailUrl'],
                                         data_dict[key]['company'],
                                         data_dict[key]['date'],
                                         data_dict[key]['jobDescription'])

                # the new urls should only be the nextURL
                if next_url is not None:
                    next_url = "http://service.dice.com" + next_url
                    self.urls.add_new_url(next_url)

                count = count + 1
            except Exception as err:
                print "craw failed"
                print err
                raise err

        self.outputer.output_html()


if __name__ == "__main__":
    root_url = ("http://service.dice.com/api/rest/"
                "jobsearch/v1/simple.json?text=java&page=2")
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
