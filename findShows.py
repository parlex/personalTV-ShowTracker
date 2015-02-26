#!/usr/bin/python

import urllib, sys

# Baseurl
baseurl = "http://www.omdbapi.com/?"

# Queries
apiVars = { 't': sys.argv[1], 'r' : 'json'}

# Query to the api requesting the show passed as arg.
query = baseurl+urllib.urlencode(apiVars)

# The Json returned by the api without curly brackets
info = urllib.urlopen(query).read()[1:-1].split(',')

# Returns the ID of the show
def getID(showInfo):
   for field in showInfo:
      if 'imdbID' in field:
         return field


print getID(info)
