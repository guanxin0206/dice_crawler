#!/usr/bin/env python -t
# -*- coding: UTF-8 -*-
import url_manager,html_downloader,html_parser,html_outputer,mysql_inserter

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.html_parser = html_parser.HtmlParser()
        self.json_parser = json_parser.JsonParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.inserter = mysql_inserter.MySQLInserter(conn)
        

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print "craw %d : %s" % (count, new_url)
                json_cont = self.downloader.download_json(new_url)

                new_data, next_url = self.json_parser(json_cont)

                for key in json_cont:
                    
                    # TODO: html_downloader returns url, html_cont
                    real_url, html_cont = self.downloader.download(new_data[key]['detailUrl'])
                    new_data[key]['detailUrl'] = real_url
                    job_description = self.html_parser.parse(new_url, html_cont)



                # Values to insert keyword, jobTitle, jobUrl, company, postDate, jobUniqueId, JobDescription
                qry = ""
                self.ins
                
                # the new urls should only be the nextURL
                self.urls.add_new_urls(new_urls)
                
                #self.outputer.collect_data(new_data)

                if next_url is None:
                    break
                count = count + 1
            except:
                print "craw failed"
                #raise

        self.outputer.output_html()

if __name__ == "__main__":
    #root_url = "http://baike.baidu.com/item/Python"
    root_url = "http://service.dice.com/api/rest/jobsearch/v1/simple.json?text=java"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
