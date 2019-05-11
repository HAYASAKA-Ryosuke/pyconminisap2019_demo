from pyconminisap import PyconMiniSap


def hello(environ):
    return "200 OK", "Hello さっぽろ!!", [('Content-Type', 'text/html')]


def show_ham(environ):
    id = environ['PATH_INFO'].split('/hams/')[1]
    return "200 OK", "IDとして{}を指定しましたね".format(id), [('Content-Type', 'text/html')]


def show_data(environ):
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    data = environ.get('wsgi.input').read(content_length).decode('utf8')
    return "200 OK", "Hello {}".format(data), [('Content-Type', 'text/html')]


application = PyconMiniSap()

application.router.add_url_pattern('/', 'GET', hello)
application.router.add_url_pattern('/hams/:ham_id/', 'GET', show_ham)
application.router.add_url_pattern('/post_data/', 'POST', show_data)
