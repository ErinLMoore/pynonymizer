#!flask/bin/python3

from httmock import response, urlmatch


NETLOC = r'(.*\.)?api\.github\.com$'
HEADERS = {'content-type': 'application/json'}
GET = 'get'

@urlmatch(netloc=NETLOC, path='/repos', method=GET)
def repository():
    file_path = url.netloc + url.path
    with open(file_path, 'r') as f:
        content = f.read()
    return response(200, content, HEADERS, None, 5, request)