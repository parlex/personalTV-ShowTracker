#!/usr/bin/python

import urllib, sys

class ShowInfo():
   def __init__(self, showname):
      # Baseurl
      self.baseurl = "http://www.omdbapi.com/?"
   
      # Queries
      self.apiVars = { 't': showname, 'r' : 'json'}
   
      # Query to the api requesting the show passed as arg.
      self.query = self.baseurl+urllib.urlencode(self.apiVars)
   
      # The Json returned by the api without curly brackets
      self.info = urllib.urlopen(self.query).read()[1:-1].split(',')

      self.showDict = self.transformToDict()
 
   # Transforms the info list to a dictionary
   def transformToDict(self):
      output = {}
      for entry in self.info:
         if 'Title' in entry or 'Poster' in entry or 'imdbRating' in entry or 'imdbID' in entry:
            output[entry.split(":")[0].strip("\"")] = entry.split(":")[1].strip("\"")
               
      return output
   
   # Returns the show title
   def getTitle(self):
      return self.showDict.get("Title")
   
   # Returns the show poster this doesn't work yet
   def getPoster(self):
      return self.showDict.get("Poster")
   
   # Returns the show  IMDB rating
   def getRating(self):
      return self.showDict.get("imdbRating")
   
   # Returns the show ID on IMDB
   def getID(self):
      return self.showDict.get("imdbID")
