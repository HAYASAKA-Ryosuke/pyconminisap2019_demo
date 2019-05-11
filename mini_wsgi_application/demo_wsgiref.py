from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello World\n']

with make_server('', 8000, application) as httpd:
    httpd.serve_forever()
