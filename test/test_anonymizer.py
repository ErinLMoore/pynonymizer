#!flask/bin/python3

import unittest
from mock import patch
from app.anonymizer import Anonymizer
import os

class testAnonymizer(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_anonymous_name(self):
        import time
        from datetime import date
        description = 'my test!abcdefghijklmnopqrstuvwxyz'
        with patch('app.anonymizer.time') as mock_time:
            with patch('app.anonymizer.date') as mock_date:
                mock_time.time.return_value = 1474998091.10703
                mock_date.today.return_value = date(2016, 9, 27)
                anonymizer = Anonymizer()
                expected = "my-test-abcdefghijklmnopqrstuv_2016-09-27_6b7c5"
                actual = anonymizer.get_anonymous_name(description)
                self.assertEqual(expected, actual)


    from httmock import all_requests
    @all_requests
    def response_content(self, url, request):
        from httmock import response
        HEADERS = {'content-type': 'application/json'}
        filename = eval(request.body)
        file_path = ("test/"+url.netloc+url.path+'/'+filename['name'])
        with open(file_path, 'r') as f:
            content = f.read()
            return response(201, content, HEADERS, None, 5, request)

    def test_create_github_repo(self):
        from httmock import HTTMock
        import requests
        with HTTMock(self.response_content):
            username = os.environ["pynonymizer_username"]
            anonymous_name = 'test_2016-09-27_6b7c5'
            anonymizer = Anonymizer()
            results = anonymizer.create_github_repo(anonymous_name)
            resultsdict = eval(results.content)
            self.assertEqual(resultsdict['full_name'], username+"/tm")
            self.assertEqual(resultsdict['name'], anonymous_name)
