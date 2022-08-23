import socket

def main():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('', 8000))
    tcp_server_socket.listen(128)

    while True:
        print("waiting a client......")
        client_socket, clientAddr =  tcp_server_socket.accept()
        print("a client is coming...")
        print(clientAddr)
        while True:
            print("waiting client ask...")
            recv_data  = client_socket.recv(1024)
            print(recv_data.decode('utf-8'))
            print("sending to client")

            if recv_data:
                client_socket.send(" hahaha ---ok---".encode("utf-8"))
            else:
                break
        client_socket.close()
    tcp_server_socket.close()

if __name__ == '__main__':
    main()