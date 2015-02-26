#!/usr/bin/python

from HTMLParser import HTMLParser
from findShows import ShowInfo as mdb
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

# Returns a shows schedule-data
def getShowData(show):
   showInfo = mdb(show)

   # Creates the url for the tvschedule of the show
   baseurl = "http://www.imdb.com/title/{0}/tvschedule".format(showInfo.getID())

   # Fetches the html of the url
   response = url.urlopen(baseurl)
   html = response.read()
   
   # Starts the parser and feeds the html
   parser = IMDBHTMLParser()
   parsedData = parser.feed(html)

   return parser.data

# Creates json of showlists
def getJSONData(showList):
    data = {}
    for show in showList:
        # Temporary dictionary that should store show-dataentries
        tmp = {}       
        # Name of previous episode - to ensure no duplicates
        prevname = ""
        # Goes through every entry where a show is aired and adds it to the output
        for entry in getShowData(show):
            # If episode isn't already stored
            if prevname != entry[3]:
                tmp['date'] = entry[0]
                tmp['time'] = entry[1]
                tmp['name'] = entry[3]
                tmp['episode'] = entry[5]
            prevname = entry[3]

        data[show] = tmp

    return json.dumps(data)
    

# Returns a formatted string of the output
def getPrettyPrint(showList):
   # Output string
   output = ""

   for show in showList:
      output += "{0}\n##############\n".format(show.upper())
      count = 0
      # Name of previous episode - to ensure no duplicates
      prevname = ""
      
      # Goes through every entry where a show is aired and adds it to the output
      for entry in getShowData(show):
         count += 1
         # If episode isn't already printed
         if prevname != entry[3]:
            output += "{0}. {1} @ {2} - {3} {4}\n".format(count, entry[0], entry[1], entry[3], entry [5]) 
         # Update previous
         prevname = entry[3]

      output += "\n"

   return output

# Favourite shows
favs = open('myshows.txt', 'r')
schedule = open('showSchedule.json', 'w')

# List of favourite shows and filtering away empty strings
showList = filter(None, favs.read().split("\n"))

schedule.write(getJSONData(showList))

# Closing files
favs.close()
schedule.close()
