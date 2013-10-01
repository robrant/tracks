import numpy as np
from scipy import integrate
import datetime
import sys


#----------------------------------------------------------------#

def loadArray(fName):
    ''' Load an array back in. Check length is OK.'''

    try:
        arr = np.load(fName)
        return arr
    except IOError, e:
        print 'Failed to find file', e

    sys.exit()

#----------------------------------------------------------------#

def extractFldsFromList(records, flds=[]):
    ''' Builds list containing a particular field and returns it.'''

    # In the event that fields aren't supplied
    if len(flds) < 1:
        print 'You must supply fields to extract'
        return None

    paramList = []

    # Loop the records
    for record in records:
        row = []
        for key in record.keys():
            if key in flds:
                row.append(record[key])

        paramList.append(row)

    return paramList

#----------------------------------------------------------------#

def fldLookup(handset=4, timeFld=None, keywords=None, fldNames=None, namesOut=None):
    ''' Return:-
            A full list of fields
            A subset based on keyword (mag, accel, geo, rate, rot)
            A subset based on specific field.
        Returns either the field names or the indexes. '''

    if keywords and fldNames:
        print "Must provide keywords or field names as arguments. Not both."

    fldsOut = []

    # The starting set of fields
    flds = ['ElapsedTime(s)','xMag(uT)', 'yMag(uT)', 'zMag(uT)',
            'xAccel(g)', 'yAccel(g)', 'zAccel(g)',
            'latitude(deg)', 'longitude(deg)', 'altitude(m)',
            'xRate(rad/sec)', 'yRate(rad/sec)', 'zRate(rad/sec)',
            'roll(rad)', 'pitch(rad)', 'yaw(rad)']

    # The starting set of fields
    kwFlds = {'time':'ElapsedTime(s)',
              'mag' :['xMag(uT)', 'yMag(uT)', 'zMag(uT)'],
              'acc' :['xAccel(g)', 'yAccel(g)', 'zAccel(g)'],
              'geo' :['latitude(deg)', 'longitude(deg)', 'altitude(m)'],
              'rate':['xRate(rad/sec)', 'yRate(rad/sec)', 'zRate(rad/sec)'],
              'rot' :['roll(rad)', 'pitch(rad)', 'yaw(rad)']
              }

    # To just return the list of all field names (2ndry purpose)
    if namesOut and not fldNames:
        if not timeFld:
            subFlds = flds
        else:
            subFlds = flds[1:]
        return subFlds

    # Subset based on keyword
    if keywords:
        fldNames = []
        for keyword in keywords:
            print keyword
            print kwFlds[keyword]
            fldNames = fldNames + kwFlds[keyword]

    # Return all the fields if none are specified
    if not fldNames:
        fldNames = flds[1:-1]

    # Loop the fields in and get their indexes
    for fld in fldNames:

        # Account for the lack of gyro in the iPhone 3G/3GS
        if handset < 4:
            if fld in kwFlds['rate'] or fld in kwFlds['rot']:
                continue

        fldsOut.append(flds.index(fld))

    # Add in the time field - at index pos 0
    if timeFld:
        fldsOut.insert(0, flds.index('ElapsedTime(s)'))
            
    return fldsOut


#----------------------------------------------------------------#


def extractFldsFromArray(arr, flds=[]):
    ''' Builds list containing a particular field and returns it.'''

    # In the event that fields aren't supplied
    if len(flds) < 1:
        print 'You must supply fields to extract'
        return None

    paramList = []

    # Loop the records
    for record in records:
        row = []
        for key in record.keys():
            if key in flds:
                row.append(record[key])

        paramList.append(row)

    return paramList

#----------------------------------------------------------------#
"""
fName = '/Users/brantinghamr/Documents/code/driveLogging/velocityDistanceTests/20120119_static_integration_test.npy'
handset = 3

fullArr = loadArray(fName)

flds = []


# Extract the relevant fields
extractFldsFromArray(fullArr, 


"""










