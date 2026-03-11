import argparse
import os
import socket
import sys
from typing import Optional

import protocol


def start_server(
    host: str,
    port: int,
    *,
    token: Optional[str],
    timeout_s: float,
    max_frame_bytes: int,
) -> int:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        try:
            conn, addr = server.accept()
        except KeyboardInterrupt:
            print("Stopping server")
            return 130

        conn.settimeout(timeout_s)
        print(f"Connection established from {addr}")

        try:
            hello = protocol.recv_json(conn, max_bytes=max_frame_bytes)
            if hello.get("type") != "hello":
                protocol.send_json(conn, {"type": "welcome", "ok": False, "error": "expected hello"})
                conn.close()
                continue

            client_token = hello.get("token")
            client_name = hello.get("client")

            if token is not None and client_token != token:
                protocol.send_json(conn, {"type": "welcome", "ok": False, "error": "bad token"})
                conn.close()
                continue

            protocol.send_json(conn, {"type": "welcome", "ok": True, "server": "py_c2"})

            cmd_id = 0
            while True:
                try:
                    command = input("py_c2> ").strip()
                except EOFError:
                    command = "exit"

                if not command:
                    continue

                if command in (":help", "help"):
                    print("Client commands: help, ping, time, sysinfo, echo <text>, exit")
                    print("Server commands: :help, :quit")
                    continue

                if command in (":quit", ":q"):
                    print("Closing connection")
                    conn.close()
                    break

                cmd_id += 1
                protocol.send_json(conn, {"type": "cmd", "id": cmd_id, "cmd": command})

                if command.lower() in ("exit", "quit"):
                    conn.close()
                    break

                res = protocol.recv_json(conn, max_bytes=max_frame_bytes)
                if res.get("type") != "result" or res.get("id") != cmd_id:
                    print(f"Unexpected response: {res}")
                    continue

                output = res.get("output")
                if output is None:
                    print("(no output)")
                else:
                    print(str(output))

        except protocol.ProtocolError as e:
            print(f"Protocol error: {e}")
        except (ConnectionResetError, BrokenPipeError):
            print("Connection closed")
        except socket.timeout:
            print("Timed out")
        except KeyboardInterrupt:
            print("Interrupted")
        finally:
            try:
                conn.close()
            except Exception:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start safe demo server (no OS command execution on client).")
    parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=12345, help="Server port number (default: 12345)")
    parser.add_argument(
        "--token",
        default=os.environ.get("PY_C2_TOKEN"),
        help="Shared token (defaults to env var PY_C2_TOKEN).",
    )
    parser.add_argument("--timeout", type=float, default=20.0, help="Socket timeout seconds (default: 20)")
    parser.add_argument(
        "--max-frame-bytes",
        type=int,
        default=1024 * 1024,
        help="Max message size in bytes (default: 1048576)",
    )
    args = parser.parse_args()

    raise SystemExit(
        start_server(
            args.host,
            args.port,
            token=args.token,
            timeout_s=args.timeout,
            max_frame_bytes=args.max_frame_bytes,
        )
    )
