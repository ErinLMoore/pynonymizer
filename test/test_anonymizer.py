#!flask/bin/python3

import unittest
from mock import patch
from app.anonymizer import Anonymizer

class testAnonymizer(unittest.TestCase):

    def setUp(self):
        anonymizer = Anonymizer()

    def test_get_anonymous_name(self):
        import time
        from datetime import date
        description = 'my test'
        with patch('app.anonymizer.time') as mock_time:
            with patch('app.anonymizer.date') as mock_date:
                mock_time.time.return_value = 1474998091.10703
                mock_date.today.return_value = date(2016, 9, 27)
                anonymizer = Anonymizer()
                expected = "my-test_2016-09-27_6b7c5"
                actual = anonymizer.get_anonymous_name(description)
                self.assertEqual(expected, actual)
