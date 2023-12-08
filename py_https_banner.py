import socket
import ssl
import argparse

def get_https_banner(host, port):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.sendall(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                banner = ssock.recv(1024)
                print(f"HTTPS Banner for {host}:{port}:\n{banner.decode('utf-8')}")
    except socket.error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve HTTPS banner')
    parser.add_argument('host', help='Target host')
    parser.add_argument('port', type=int, help='Target port')
    


    args = parser.parse_args()

    get_https_banner(args.host, args.port)

