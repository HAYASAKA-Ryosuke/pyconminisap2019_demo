
# gunicorn demo_gunicorn
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello World\n']

# 下記はクラス構文例
# class Application:

#     def __call__(self, environ, start_response):
#         start_response('200 OK', [('Content-Type', 'text/plain')])
#         return [b'HelloWorld']
# 
# application = Application()
