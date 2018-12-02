# coding: utf-8
import socket

host = ''
port = 2000

s = socket.socket()

s.bind((host, port))

while True:
    s.listen(5)
    connection, address = s.accept()
    print("type connection {}".format(type(connection)))
    request = connection.recv(1024)
    print('ip and address {} \n {}'.format(address, request.decode('utf-8')))
    response = b'HTTP/1.1 200 ok \r\n\r\n<h1> HELLO WORLD'
    connection.sendall(response)
    connection.close()


