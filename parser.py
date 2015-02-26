#!/usr/bin/python

from HTMLParser import HTMLParser
from findShows import IMDBShowInfo as imdb
import urllib2 as url, json

class IMDBHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # Lists to store the info about the schedule
        self.data = []
        self.current = []

        # If the parser is in a row/col of a table
        # we updates the data sets
        self.inTRow = False
        self.inTcol = False
    
    # What to do with when startag is found
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            if len(attrs) > 0:
                self.inTRow = True
        elif tag == 'td':
            self.inTcol = True

    # What to do with when endtag is found
    def handle_endtag(self, tag):
        if tag == 'tr':
            # We are now about to leave the row so
            # we need to store the current data as a list
            # in the dataset and set row to false
            if self.inTRow:
               self.data.append(self.current)
               self.current = []
            self.inTRow = False
        elif tag == 'td':
            self.inTcol = False

    # What to do with when inbetween start- and endtag
    def handle_data(self, data):
        # If we are in a coloumn and a row the data is stored as
        # current list
        if self.inTcol and self.inTRow:
            self.current.append(data)

# Gets the show's info
show = imdb("suits")

# Creates the url for the tvschedule of the show
baseurl = "http://www.imdb.com/title/{0}/tvschedule".format(show.getID())

# Fetches the html of the url
response = url.urlopen(baseurl)
html = response.read()


# Starts the parser and feeds the html
parser = IMDBHTMLParser()
parsedData = parser.feed(html)

# Prints to test if it works
for dataentry in parser.data:
    date = dataentry[0]
    time = dataentry[1]
    channel = dataentry[2]
    name = dataentry[3]
    episode = dataentry[5]

    print "Date : {0}\nTime: {1}\nName: {2} {3}\n\n".format(date, time, name, episode)
