import socket
import threading

HOST = '127.0.0.1'
PORT = 50000

# 创建 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定主机地址和端口
server_socket.bind((HOST, PORT))

# 监听客户端连接请求
server_socket.listen(5)

# 记录所有已连接的客户端
clients = []

def handle_client(client):
    while True:
        try:
            # 接收客户端消息
            message = client.recv(1024).decode()
            if message:
                # 广播消息给所有客户端
                # print("收到来自"+client.fileno()+"的信息")
                print(message+"\n")
                for c in clients:
                    if c != client:
                        c.sendall(bytes(message, 'utf-8'))
            else:
                # 客户端断开连接
                print(f'[DISCONNECTED] {client.getpeername()} disconnected.'+"\n")
                clients.remove(client)
                client.close()
                break
        except Exception as e:
            print(f'[ERROR] {e}'+"\n")
            break

while True:
    try:
        # 等待客户端连接
        print('[INFO] Waiting for connection...'+"\n")
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()
        print(f'[CONNECTED] {address} connected to the server.'+"\n")
    except KeyboardInterrupt:
        # 关闭服务端
        for c in clients:
            c.close()
        server_socket.close()
        print('\n[SERVER STOPPED]'+"\n")
        break
