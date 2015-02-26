#!/usr/bin/python

from HTMLParser import HTMLParser
import urllib2 as url
import json

response = url.urlopen("http://www.imdb.com/title/tt1358522/tvschedule")
html = response.read()

class IMDBHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.data = []
        self.current = []

        self.inTRow = False
        self.inTcol = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            if len(attrs) > 0:
                self.inTRow = True
        elif tag == 'td':
            self.inTcol = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            if self.inTRow:
                self.data.append(self.current)
                self.current = []
            self.inTRow = False
        elif tag == 'td':
            self.inTcol = False

    def handle_data(self, data):
        if self.inTcol and self.inTRow:
            self.current.append(data)


parser = IMDBHTMLParser()
parsedData = parser.feed(html)

for dataentry in parser.data:
    date = dataentry[0]
    time = dataentry[1]
    channel = dataentry[2]
    name = dataentry[3]
    episode = dataentry[5]

    print "Date : {0}\nTime: {1}\nName: {2} {3}\n\n".format(date, time, name, episode)

