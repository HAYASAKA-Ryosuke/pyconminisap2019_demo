import sys
import socket
import urllib.parse
from io import BufferedReader, BytesIO
from hello import application


class WSGIServer:
    RECIEVE_LENGTH = 4096
    LISTEN_NUMBER = 1

    def setup_socket(self, ip, port):
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port,))
        server.listen(self.LISTEN_NUMBER)
        return server

    def __init__(self, ip, port, application):
        self.ip = ip
        self.port = int(port)
        self.application = application
        self.environ = dict()
        self.socket = self.setup_socket(ip, port)
        self.status_and_headers = []

    def get_environ(self, stream):
        environ = dict()
        stream_list = stream.decode('utf-8').split('\r\n')
        environ['REQUEST_METHOD'] = stream_list[0].split(' ')[0]
        environ['PATH_INFO'] = urllib.parse.urlparse(stream_list[0].split(' ')[1]).path
        environ['QUERY_STRING'] = urllib.parse.urlparse(stream_list[0].split(' ')[1]).query
        environ['SERVER_PROTOCOL'] = 'http'
        environ['SERVER_NAME'] = self.ip
        environ['SERVER_PORT'] = int(self.port)
        environ['CONTENT_LENGTH'] = len(stream_list[-1].encode('utf-8'))
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.url_scheme'] = 'http'
        environ['wsgi.input'] = BufferedReader(BytesIO(stream_list[-1].encode('utf-8')))
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = False
        environ['wsgi.run_once'] = False

        return environ

    def start_response(self, status, response_headers):
        self.status_and_headers = [status, response_headers]

    def send_response(self, connect, datas):
        status, headers = self.status_and_headers
        status_response = 'HTTP/1.1 {}\r\n'.format(status)
        header_response = ''.join(map(lambda header: '{}: {}\r\n'.format(*header), headers))
        body = ''.join(map(lambda data: '{}\r\n'.format(data.decode('utf-8')), datas))
        response = "{}{}\r\n{}".format(status_response, header_response, body)
        connect.sendall(response.encode('utf-8'))

    def serve(self):
        connect, address = self.socket.accept()
        self.socket.close()
        stream = connect.recv(self.RECIEVE_LENGTH)
        self.environ = self.get_environ(stream)
        datas = self.application(self.environ, self.start_response)
        self.send_response(connect, datas)

if __name__ == '__main__':
    wsgi_server = WSGIServer('127.0.0.1', 8000, application)
    wsgi_server.serve()
