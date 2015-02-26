#!/usr/bin/python

import urllib, sys

#baseurl
baseurl = "http://www.omdbapi.com/?"

#queries
apiVars = { 't': sys.argv[1], 'r' : 'json'}

# Query to the api requesting the show passed as arg.
query = baseurl+urllib.urlencode(apiVars)

# The Json returned by the api without curly brackets
data = urllib.urlopen(query).read()[1:-1].split(',')

# Just printing all the data about the show
for d in data:
   print d
