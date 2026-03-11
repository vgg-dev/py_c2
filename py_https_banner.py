import argparse
import socket
import ssl
from typing import Optional


def get_https_banner(host: str, port: int, *, timeout_s: float, max_bytes: int, path: str) -> int:
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout_s) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                req = (
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    "User-Agent: py_https_banner/1.1\r\n"
                    "Connection: close\r\n\r\n"
                ).encode("utf-8")
                ssock.sendall(req)

                chunks: list[bytes] = []
                received = 0
                while received < max_bytes:
                    data = ssock.recv(min(4096, max_bytes - received))
                    if not data:
                        break
                    chunks.append(data)
                    received += len(data)

                banner = b"".join(chunks)
                print(f"HTTPS Banner for {host}:{port} (up to {max_bytes} bytes):\n")
                print(banner.decode("utf-8", errors="replace"))
        return 0

    except (socket.timeout, TimeoutError):
        print("Error: timed out")
        return 1
    except ssl.SSLError as e:
        print(f"TLS error: {e}")
        return 1
    except OSError as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve an HTTPS banner (TLS + basic HTTP request).")
    parser.add_argument("host", help="Target host")
    parser.add_argument("port", type=int, nargs="?", default=443, help="Target port (default: 443)")
    parser.add_argument("--path", default="/", help="HTTP path (default: /)")
    parser.add_argument("--timeout", type=float, default=8.0, help="Timeout seconds (default: 8)")
    parser.add_argument("--max-bytes", type=int, default=8192, help="Max bytes to read (default: 8192)")
    args = parser.parse_args()

    raise SystemExit(get_https_banner(args.host, args.port, timeout_s=args.timeout, max_bytes=args.max_bytes, path=args.path))
