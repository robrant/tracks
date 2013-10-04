'''
Created on Oct 3, 2013

@author: robrant
'''
import unittest
from setup import setup_database

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_build_db(self):

        db, cursor = setup_database.build_db()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_build_db']
    unittest.main()