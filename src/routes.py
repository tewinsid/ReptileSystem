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
