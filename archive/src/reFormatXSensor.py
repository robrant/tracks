
import os
import datetime
import numpy as np
from scipy import integrate

#----------------------------------------------------------------#

def getFldIndex(line):
    ''' Gets the field index into a list '''

    


#----------------------------------------------------------------#

def getDictionary(line):
    ''' Builds a dictionary from the fields found in the file '''

    fldString = ''
    line = line.strip('\n')
    flds = line.split(' ')

    # Loop the field names and add them to a dictionary
    for fld in flds:
        # Build a string for the csv
        fldString += fld+','

    fldString = fldString.rstrip(',')

    return flds, fldString

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

def fileHandler(dirName, fileName, csvOut=None, listOut=None,
                npArray=None, npSaved=None):

    ''' Reads in the data and gets it out to various formats.
            1. Csv out for an xls/numbers spreadsheet (automated posting to GDocs?)
            2. Numpy array in memory
            3. Numpy array saved to an object
            
        Can also specify whether you just want certain fields output
        to cut down on the data volumes while testing.
        In future, maybe also ability to set the sampling rate from the file?
        Add in some checks for <null>??
        
    ''' 

    # Open the file
    try:
        f = open(os.path.join(dirName, fileName),'r')
    except:
        print 'Failed to open the file. Placeholder for error reporting'

    # Outfile common name (whether for .csv or .npy)
    outFileName = os.path.join(dirName, fileName[:-4])


    #Handle the arguments
    if csvOut:
        textOut = []

    if npArray or npSaved:
        npOut=[]

    if listOut:
        dataOut=[]
    else: dataOut = None
        
    #Line counter and output lists
    i = 0

    # Loop the lines in the file:
    for line in f.readlines():


        # Deal with the description line
        if i==0:
            startDate = getStartTime(line)
            #print line

        # Get a blank dictionary of the fields, a list of flds and a string version
        elif i==1:
            flds, fldsText = getDictionary(line)
            #print flds
        else:

            # Strip off the carriage return
            line = line.rstrip('\n')
            
            # Split the contents of each line based on a space
            splitLine = line.split(' ')

            # Build dataOut: a list of dictionaries of data
            d = {}
            floatData = []
            lineText = ''
            
            for j in range(len(splitLine)):

                fldName = flds[j]

                #Create a float version of the line
                if npArray or npSaved:
                    floatData.append(float(splitLine[j]))

                # For memory list/dict
                if listOut:
                    d[fldName] = float(splitLine[j])

                # For csv output for better xls/numbers viewing
                if csvOut:
                    lineText += str(splitLine[j])+','

            # For memory list/dict or numpy output
            if listOut:        
                dataOut.append(d)

            if npArray or npSaved:
                npOut.append(floatData)

            if csvOut:
                #Strip the last comman            
                lineText = lineText.rstrip(',')

                # This just builds a list of strings
                textOut.append(lineText)
     
        i+=1

    # Close the file
    f.close()

              
    # Return the name of the output file having created it.
    if csvOut:

        csvFileName = outFileName+'.csv'
        # Deal with the write out for a spreadsheet
        outCsvFile = open(csvFileName, 'w')

        # Write to file
        outCsvFile.write(fldsText +'\n') # Field names
        # Data lines
        for outLine in textOut:
            outCsvFile.write(outLine + '\n')

        # Close out the out file.
        outCsvFile.close()
    else:
        csvFileName = None

    

    # Return a numpy array in memory
    if npArray or npSaved:
        arr = np.array(npOut)

        if npSaved != None and npArray != None:
            np.save(outFileName, arr)
            npArray = arr
            outFileName+='.npy'
            
        elif npSaved != None and npArray == None:
            npArray = None
            outFileName+='.npy'
            
        elif npSaved == None and npArray != None:
            outFileName = None
            
    else:
        npArray = None
        outFileName = None


    return csvFileName, dataOut, npArray, outFileName


#------------------------------------------------------------------------------#

dirName = "/Users/brantinghamr/Documents/code/driveLogging/"
fileName= "20111208_am_focus_ip4_front_acrossTown.txt"

dirName = "/Users/brantinghamr/Documents/code/driveLogging/velocityDistanceTests/"
fileName= "20120119_static_integration_test.txt"


a, b, c, d = fileHandler(dirName, fileName, csvOut=None, listOut=False,
                npArray=None, npSaved=True)
print d

# Get out particular fields from the dictionary
#fieldsOfInterest = extractFlds(b, ['xAccel(g)','yAccel(g)','zAccel(g)'])


# Get out xAcc
#xAcc = extractFlds(b, ['xAccel(g)'])

#xAcc = np.array(xAcc)

#print xAcc.shape
    
    # Get out a particular parameter from the dictionary:
    #xAcc = extractParameter(dataOut, 'xAccel(g)')


