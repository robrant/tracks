
# Standard
import sys
import os
import datetime
import json

import sys
projectPath = '/Users/robrant/eclipseCode/tracks/loggerIngest'
if projectPath not in sys.path:
    sys.path.append(projectPath)

# OSS
#import geojson

# Custom
from config import ingestSettings as settings
import inserters

#----------------------------------------------------------------#

def getDictionary(line):
    ''' Builds a dictionary from the fields found in the file '''

    # Placeholder for output field names
    fldsOut = []
    fldUnits = {}

    # remove the carriage return and split into a list
    line = line.strip('\n')
    flds = line.split(' ')

    # Add all the field names to a list and build a dict of fld name to the field unit
    for fld in flds:
        fldName, fldUnit = fld.split('(')
        fldsOut.append(fldName)
        fldUnits[fldName] = fldUnit.rstrip(')')

    return fldsOut, fldUnits

#----------------------------------------------------------------#

def getStartTime(line):
    ''' Extracts the start timestamp from the first line (0) '''

    # Looks like:
    # iPhone Sensor Log from Crossbow started at 8 Jan 2012 09:21:30 Greenwich Mean Time.

    # Split the line into elements based on spaces
    line = line.split(' ')
    
    # Kludge the elements together
    dt = line[7] + line[8] + line[9] + line[10]

    # Return a datetime object
    start = datetime.datetime.strptime(dt, '%d%b%Y%H:%M:%S')
    
    return start    

#----------------------------------------------------------------#

def getTimeStamp(startTime, elapsedTime):
    ''' Gathers the absolute timestamp of the observation'''
    
    timeDelta = datetime.timedelta(seconds=float(elapsedTime))
    obsTime = startTime + timeDelta

    return obsTime.isoformat()

#----------------------------------------------------------------#

def getGeoJson(lon, lat):
    ''' Build geojson from the lon and lat'''

    p = geojson.Point([float(lon), float(lat)])
    return geojson.dumps(p)


#----------------------------------------------------------------#

def extractData(dirName, fileName):

    ''' Loops file and outputs json/dict object of content.
    ''' 

    # Open the file
    try:
        f = open(os.path.join(dirName, fileName),'r')
    except:
        print 'Failed to open the file. Placeholder for error reporting'

    #Line counter and output lists
    i = 0
    output = []

    # Loop the lines in the file:
    for line in f.readlines():

        # Deal with the description line
        if i==0:
            startDate = getStartTime(line)
            #print line

        # Get a blank dictionary of the fields, a list of flds and a string version
        elif i==1:
            flds, fldUnits = getDictionary(line)
            #print flds
        else:

            # Strip off the carriage return
            d = {}
            line = line.rstrip('\n')
            splitLine = line.split(' ')

            # Build dataOut: a list of dictionaries of data
            for j in range(len(splitLine)):
                fldName = flds[j]

                # For memory list/dict
                if splitLine[j] != '(null)': 
                    d[fldName] = float(splitLine[j])
                else:
                    d[fldName] = None
                    
                # Set the field for absolute timestamp
                if fldName == settings.ELAPSED_TIME_FIELD:
                    d[settings.ABS_TIMESTAMP_FIELD] = getTimeStamp(startDate, splitLine[j])

            # Build geojson for location
            if d[settings.LON_FIELD] != None and d[settings.LAT_FIELD] != None:
                d[settings.GEO_FIELD] = getGeoJson(d[settings.LON_FIELD], d[settings.LAT_FIELD])

            output.append(d)
     
        i+=1

    # Close the file
    f.close()

    return output

#------------------------------------------------------------------------------#

def main():
    #dirName = "/Users/robrant/eclipseCode/tracks/archive/devData"
    #fileName= "20111208_am_focus_ip4_front_acrossTown.txt"

    dirName = "/Users/robrant/eclipseCode/tracks/archive/devData"
    fileName= "xBowSensorLog.txt"

    # Extract the data from the file
    data = extractData(dirName, fileName)
    #for x in data:
    #    print x
    results = inserters.postgresInserter(data)
        
    # Insert the data into postgres
    
    
    
if __name__ == '__main__':
    main()
