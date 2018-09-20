# coding: utf-8
# server.py

import socket

HOST, PORT = '', 8888
# 初始化
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 绑定
listen_socket.bind((HOST, PORT))
# 监听
listen_socket.listen(1)
print ('Serving HTTP on port %s ...' % PORT)
while True:
    try:
        # 接受请求
        client_connection, client_address = listen_socket.accept()
        # 通信
        request = client_connection.recv(1024)
        print (request.decode("utf-8"))

        http_response = """
HTTP/1.1 200 OK

Hello, World!
"""
        client_connection.sendall(http_response.encode("utf-8"))
        # 关闭连接
        client_connection.close()
    except:
        break
