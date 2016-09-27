#!flask/bin/python3

import unittest
from mock import patch
from app.anonymizer import Anonymizer

class testAnonymizer(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_anonymous_name(self):
        import time
        from datetime import date
        description = 'my test!'
        with patch('app.anonymizer.time') as mock_time:
            with patch('app.anonymizer.date') as mock_date:
                mock_time.time.return_value = 1474998091.10703
                mock_date.today.return_value = date(2016, 9, 27)
                anonymizer = Anonymizer()
                expected = "my-test-_2016-09-27_6b7c5"
                actual = anonymizer.get_anonymous_name(description)
                self.assertEqual(expected, actual)

    import test.mockgithub
    from httmock import with_httmock
    @with_httmock(test.mockgithub.repository)
    def test_create_github_repo(self):
        username = 'Anonymous-Katas'
        anonymous_name = 'test_2016-09-27_6b7c5'
        anonymizer = Anonymizer()
        results = anonymizer.create_github_repo(anonymous_name)
        self.assertTrue('name' in results)
        self.assertEqual(results['name'], anonymous_name)
