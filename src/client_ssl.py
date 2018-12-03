# coding: utf-8
import socket
import ssl


def parsed_url(url):
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    prot_dict = {
        'http': 80,
        'https': 443,
    }

    port = prot_dict[protocol]

    if ':' in host:
        h = host.split(':')
        port = int(h[1])
        ip = h[0]
    else:
        ip = host
    # return tuple
    return protocol, ip, port, path


def socket_by_protocol(protocol):
    if protocol == 'http':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = ssl.wrap_socket(socket.socket())
    return s


def get(url):
    protocol, host, port, path = parsed_url(url)
    s = socket_by_protocol(protocol)
    s.connect((host, port))
    # 不配置connection: close 则保持连接 75s才会自动关闭
    http_request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'

    s.send(http_request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)
    status_code, headers, body = parse_by_response(r)

    if status_code in [301, 302]:
        url = headers['Location']

        return get(url)

    return status_code, headers, body


def parse_by_response(r):
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = int(h[0].split(' ')[1])
    headers = {}

    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v

    return status_code, headers, body


def response_by_socket(s):
    result = b''
    buffer_size = 1024
    while True:
        response = s.recv(buffer_size)
        if len(response) == 0:
            break
        result += response
    return result


# 单元测试 以 test开头
def test_parsed_url():
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_item = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),

        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path))
    ]
    for t in test_item:
        url, expect = t
        u = parsed_url(url)
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expect)
        assert u == expect, e


def test_get():
    test_item = [
        # "http://baidu.com",
        # "http://www.baidu.com",
        "http://movie.douban.com/top250",
    ]
    for t in test_item:
        status_code, headers, body = get(t)
        print(" test_get status_code ", status_code)
        print(" test_get headers ({})".format(headers))
        print(" test_get body ", body)


def test():
    # test_parsed_url()
    test_get()


if __name__ == '__main__':
    test()
