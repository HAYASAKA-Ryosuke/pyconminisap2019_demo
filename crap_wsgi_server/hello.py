from bottle import route, default_app

@route("/")
def hello():
    return 'hello world!!'

application = default_app()
