# coding: utf-8
import socket
import os


# 程序只应该有一个入口，其他都封装为函数（传入参数，回传结果）
def run(host, port):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            log('ip and address {} \n {}'.format(address, request.decode('utf-8')))
            try:
                # chrome有时会发送空请求
                # try防止程序崩溃
                path = request.decode('utf-8').split()[1]
                log('path', path)
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            finally:
                connection.close()


def response_for_path(path):
    # 路由path到处理函数
    r = {
        '/': route_index,
        '/doge.gif': route_image
    }
    response = r.get(path, error)
    return response()


def route_index():
    header = 'HTTP/1.1 200 ok\r\nContent-Type text/html\r\n'
    body = '<h1>HELLO WORLD</h1><img src="/doge.gif"/>'
    r = header + '\r\n' + body
    return r.encode('utf-8')


def route_image():
    log('route_image')
    with open('../image/doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
    return img


# 默认参数
def error(code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND \r\n\r\n<h1> NOT FOUND</h1>'
    }
    return e.get(code, b'')


def log(*args, **kwargs):
    print('log', *args, **kwargs)


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
