#encoding=utf-8
"""
Created on 2016/3/21 15:01
author: iKexinLL
"""

import os
import flaskr
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        #assert r'No entries here so far' in rv.data, r'a'

if __name__ == '__main__':
    unittest.main()
