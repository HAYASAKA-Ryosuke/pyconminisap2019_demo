import re


class Router:

    url_patterns = []

    def add_url_pattern(self, path, method, view):
        # :fooのようにIDが指定されている部分を正規表現に置き換える
        for key in re.findall(':[a-zA-Z_]*', path):
            path = path.replace(key, '([a-z-A-Z0-9_]+)')
        path += '?' if path[-1] == '/' else path + '/?'  # /があっても無くてもマッチできるようにする
        path = '^' + path + '$'  # 開始と終わりを示す文字を追加
        self.url_patterns.append(dict(path=path, method=method, view=view))

    def search(self, path, method):
        for url_pattern in self.url_patterns:
            if bool(re.match(url_pattern['path'], path)) is True and url_pattern['method'] == method:
                return url_pattern['view']
        return None


class PyconMiniSap:

    def __init__(self):
        self.router = Router()

    def __call__(self, environ, start_response):

        # 指定されたPATHとメソッドを渡して対応するview関数を呼び出す
        view = self.router.search(environ['PATH_INFO'], environ['REQUEST_METHOD'])

        if view is not None:
            status_code, body, header = view(environ)
        else:
            status_code, body, header = ('404 Not Found', '', [('Content-Type', 'text/html')])

        start_response(status_code, header)

        return [body.encode('utf8')]
