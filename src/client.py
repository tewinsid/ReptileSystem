# coding: utf-8
import socket

#socket.AF_INET ipv4,socket.SOCK_STREAM tcp
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 2000

s.connect((host, port))

ip, port = s.getsockname()
print('本机 IP 和 端口号 {} {}'.format(ip, port))
http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
request = http_request.encode('utf-8')
print('请求', request)

s.send(request)

response = s.recv(1024)
print('相应', response)
print('相应str', response.decode('utf-8'))
