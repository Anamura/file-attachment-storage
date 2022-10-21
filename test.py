# coding=utf-8
import os
import unittest

import app


class TestCase(unittest.TestCase):
    def setUp(self):
        from config import config_master

        self.master = config_master
        self.prod_config = config_master.load()
        self.app = app.app.test_client()

    def tearDown(self):
        if os.path.exists("./test.cfg"):
            os.remove("./test.cfg")

    def test_file_download(self):
        with self.app as c:
            resp = c.get('/download', data=(), follow_redirects=True)
            self.assertTrue(session.get('originUrl'),
                            msg="pw: {1}. session: {2}")
        self.assertEqual(True, False)

    def test_adfs_login(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
