# coding: utf-8
import socket
import os
import urllib
import utiltool


# 程序只应该有一个入口，其他都封装为函数（传入参数，回传结果）
def run(host, port):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            request = b''
            buffer_size = 1024
            while True:
                r = connection.recv(buffer_size)
                if len(request) == 0:
                    break
                request += r
            log('ip and address {} \n {}'.format(address, request.decode('utf-8')))
            try:
                # chrome有时会发送空请求
                # try防止程序崩溃
                request = request.decode('utf-8')
                if len(request.split()) < 2:
                    continue
                path = request.split()[1]
                requestObject.method = request.split()[0]
                requestObject.body = request.split('\r\n\r\n', 1)[1]
                log('path', path)
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            finally:
                connection.close()


# Request类继承于object
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    # body a=1&b=2
    def form(self):
        body = self.body
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            k, v = map(urllib.parse.unquote, (k, v))
            f[k] = v
        return f


requestObject = Request()


def response_for_path(path):
    path, query = parse_path(path)
    requestObject.path = path
    requestObject.query = query
    log('path and query', path, query)
    # 路由path到处理函数
    r = {
        '/static': route_static,
        # '/': route_index,
        # '/doge.gif': route_image
    }
    route_dict = {
        '/': route_index,
        # '/login': route_login,
        # '/register': route_register,
        # '/messages': route_message,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response()


def route_static():
    pass


def parse_path(path):
    index = path.index('?')
    if index == -1:
        return path, {}
    path, query_string = path.split('?', 1)
    query = {}
    args = query_string.split('&')
    for arg in args:
        k, v = arg.split('=')
        k, v = map(urllib.parse.unquote, (k, v))
        query[k] = v
    return path, query


def main():
    config = {
        'host': '127.0.0.1',
        'port': 2000,
    }
    run(**config)


def test():
    module_path = os.path.abspath('..')
    # module_path = os.path.dirname(__file__)
    filename = module_path + '/image/test.out'
    with open("../image/doge.gif", 'rb') as f:
        log(f.read())


if __name__ == '__main__':
    main()
