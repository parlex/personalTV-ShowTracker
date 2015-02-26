#!/usr/bin/python
import sys

# Opens file for appending
favourites = open('myshows.txt', 'a')

# Goes through all arguments given and appends the args to the file
for arg in sys.argv[1:]:
    favourites.write(arg + "\n")

# Closing the writer
favourites.close()
