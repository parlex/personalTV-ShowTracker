#!/usr/bin/python
import sys, os
shows = 'myshows.txt' 

# Opens file for appending and appends parameter given
def addShow(showName):
    with open(shows, 'a') as favs:
        favs.write(showName + "\n")
        favs.close()

# Deletes a show in the file, name of show given as parameter.
def deleteShow(showName):
    # It didn't work to edit in the file so had to make a new one...
    tmpFile = 'tmp.txt'
    with open(shows, 'r') as fav:
        with open(tmpFile, 'w+') as favs:
            for line in fav:
                if not showName in line: 
                    favs.write(line)
                else:
                    print('Deleted entry for show with name ' + showName)
            favs.close()
    fav.close()

    os.remove(shows)
    os.rename(tmpFile, shows)

# Formats the text explaining the commands.
def commands():
    header = 'Commands'.center(20,'-')
    cmds = 'add: Add show.\ndel: Delete show.'
    helper = 'Select \'add\' or \'del\' (q to quit): '
    return raw_input('{}\n{}\n{}'.format(header, cmds, helper))

# Parses and executes action from command given by user
def loop():
    cmd = commands()
    while 'q' not in cmd:
        if 'add' in cmd:
            addShow(raw_input('Add show: '))
        elif 'del' in cmd:
            deleteShow(raw_input('Delete show: '))
        else:
            print('Command not recognized!')
        cmd = commands() 

# Starts loop
loop()
