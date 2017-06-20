#!/usr/bin/env python -t
# -*- coding: UTF-8 -*-
import codecs
import urllib

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self,data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = open('output.html','w')
        """
        for data in self.datas:
            print data['url'].encode("utf-8"),  type(data['url'].encode("utf-8"))
            print urllib.unquote(data['url'].encode("utf-8")) ,type(urllib.unquote(data['url'].encode("utf-8")))
            #print urllib.unquote(data['url']).encode("utf-8") , type(urllib.unquote(data['url']).encode("utf-8"))
            #print data['title'],type(data['title'])
            #print data['summary'],type(data['summary'])
        """
        
        fout.write("<html>")
        fout.write("<head>")
        
        fout.write("<meta charset='UTF-8'>")
        fout.write("</head>")
        fout.write("<body>")
        fout.write("<table>")
        
        # 默认编码ascii
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % urllib.unquote(data['url'].encode('utf-8')))
            fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
            fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()
        

