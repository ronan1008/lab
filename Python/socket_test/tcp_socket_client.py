import socket

def main():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('', 8000))
    tcp_server_socket.listen(128)
    client_socket, clientAddr =  tcp_server_socket.accept()


if __name__ == '__main__':
    main()