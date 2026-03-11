import argparse
import os
import platform
import socket
import sys
import time
from typing import Optional

import protocol


def _safe_handle_command(cmd: str) -> tuple[bool, str]:
    """Return (should_exit, output)."""
    cmd = (cmd or "").strip()
    if not cmd:
        return False, ""

    parts = cmd.split(" ", 1)
    name = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    if name in ("exit", "quit"):
        return True, "bye"

    if name == "help":
        return False, "Commands: help, ping, time, sysinfo, echo <text>, exit"

    if name == "ping":
        return False, "pong"

    if name == "time":
        return False, time.strftime("%Y-%m-%d %H:%M:%S %z")

    if name == "sysinfo":
        return False, (
            f"platform={platform.platform()}\n"
            f"python={platform.python_version()}\n"
            f"executable={sys.executable}"
        )

    if name == "echo":
        return False, arg

    return False, f"Unknown command: {name}. Try: help"


def start_client(
    server_host: str,
    server_port: int,
    *,
    token: Optional[str],
    client_name: str,
    timeout_s: float,
    max_frame_bytes: int,
    verbose: bool,
) -> int:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(timeout_s)

    try:
        client.connect((server_host, server_port))
    except OSError as e:
        print(f"Failed to connect to {server_host}:{server_port}: {e}")
        return 1

    print(f"Connected to server {server_host}:{server_port}")

    try:
        protocol.send_json(client, protocol.make_hello(token, client_name))
        welcome = protocol.recv_json(client, max_bytes=max_frame_bytes)
        if welcome.get("type") != "welcome" or not welcome.get("ok"):
            print(f"Handshake failed: {welcome}")
            return 1

        while True:
            msg = protocol.recv_json(client, max_bytes=max_frame_bytes)
            if msg.get("type") != "cmd":
                if verbose:
                    print(f"Ignoring message: {msg}")
                continue

            cmd_id = msg.get("id")
            cmd = str(msg.get("cmd") or "")
            should_exit, output = _safe_handle_command(cmd)

            protocol.send_json(
                client,
                {
                    "type": "result",
                    "id": cmd_id,
                    "ok": True,
                    "output": output,
                },
            )

            if should_exit:
                break

    except protocol.ProtocolError as e:
        print(f"Protocol error: {e}")
        return 1
    except (ConnectionResetError, BrokenPipeError):
        print("Connection closed")
        return 1
    except socket.timeout:
        print("Timed out waiting for server")
        return 1
    except KeyboardInterrupt:
        print("Interrupted")
        return 130
    finally:
        try:
            client.close()
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start safe demo client (no OS command execution).")
    parser.add_argument("--server-host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--server-port", type=int, default=12345, help="Server port number (default: 12345)")
    parser.add_argument(
        "--token",
        default=os.environ.get("PY_C2_TOKEN"),
        help="Shared token (defaults to env var PY_C2_TOKEN).",
    )
    parser.add_argument("--name", default=socket.gethostname(), help="Client name (default: hostname)")
    parser.add_argument("--timeout", type=float, default=20.0, help="Socket timeout seconds (default: 20)")
    parser.add_argument(
        "--max-frame-bytes",
        type=int,
        default=1024 * 1024,
        help="Max message size in bytes (default: 1048576)",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    raise SystemExit(
        start_client(
            args.server_host,
            args.server_port,
            token=args.token,
            client_name=args.name,
            timeout_s=args.timeout,
            max_frame_bytes=args.max_frame_bytes,
            verbose=args.verbose,
        )
    )
