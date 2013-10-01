from integrateDev import *
import unittest

#fldLookup(handset=4, timeFld=None, keywords=None, fldNames=None, namesOut=None)

#class testIntegrate(unittest.TestCase):

    
flds = fldLookup(handset=4)
truth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
print 'Handset4 without time',flds

flds = fldLookup(handset=4, timeFld=1)
truth = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
print 'Handset4 with time',flds

flds = fldLookup(handset=3)
truth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print 'Handset3', flds

flds = fldLookup(handset=3, timeFld=1)
truth = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print 'Handset3 with time', flds

#------------------------------------------------
# FIELD NAME QUERIES
#------------------------------------------------

fldsIn = 'xAccel(g)', 'yAccel(g)', 'zAccel(g)'
flds = fldLookup(handset=4, fldNames=fldsIn)
truth = [4, 5, 6]
print 'Handset4 with Accel and time', flds

fldsIn = 'latitude(deg)', 'longitude(deg)', 'altitude(m)'
flds = fldLookup(handset=4, fldNames=fldsIn)
truth = [7, 8, 9]
print 'Handset4 with lla and time', flds

fldsIn = 'xMag(uT)', 'yMag(uT)', 'zMag(uT)'
flds = fldLookup(handset=4, fldNames=fldsIn)
truth = [1, 2, 3]
print 'Handset4 with Mag and time', flds

fldsIn = 'roll(rad)', 'pitch(rad)', 'yaw(rad)'
flds = fldLookup(handset=4, fldNames=fldsIn)
truth = [13, 14, 15]
print 'Handset4 with Roll/Pitch/Yaw and time', flds

fldsIn = 'xRate(rad/sec)', 'yRate(rad/sec)', 'zRate(rad/sec)'
flds = fldLookup(handset=4, fldNames=fldsIn)
truth = [10, 11, 12]
print 'Handset4 with Gyro Rate and time', flds

#------------------------------------------------
# KEYWORD QUERIES
#------------------------------------------------

keyword = ['rot',]
flds = fldLookup(handset=4, keywords=keyword)
truth = [13, 14, 15]
print flds

keyword = ['rot',]
flds = fldLookup(handset=4, timeFld=1, keywords=keyword)
truth = [0, 13, 14, 15]
print 'Keyword extraction "rot" + time', flds

keyword = ['acc','rot']
flds = fldLookup(handset=4, timeFld=1, keywords=keyword)
truth = [0, 4, 5 ,6, 13, 14, 15]
print 'Multi-keyword extraction "acc" + "rot" + time', flds

