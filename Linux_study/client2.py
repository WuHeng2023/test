import socket
import threading

HOST = '127.0.0.1'
PORT = 50000

def receive_message(client_socket):
    while True:
        try:
            # 接收服务端消息
            message = client_socket.recv(1024).decode()
            if message:
                print(message+"\n")
            else:
                # 服务端关闭连接
                client_socket.close()
                break
        except Exception as e:
            print(f'[ERROR] {e}'+"\n")
            break

# 连接服务端
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 开启接收线程
threading.Thread(target=receive_message, args=(client_socket,)).start()

while True:
    try:
        # 发送消息给服务端
        message = "A message from client2:\n"+input()
        client_socket.sendall(bytes(message, 'utf-8'))
    except KeyboardInterrupt:
        # 关闭客户端
        client_socket.close()
        print('\n[DISCONNECTED] Disconnected from the server.')
        break
