import json
import socket
import struct
from typing import Any, Dict, Optional


PROTO_VERSION = 1


class ProtocolError(Exception):
    pass


def send_json(sock: socket.socket, obj: Dict[str, Any]) -> None:
    data = json.dumps(obj, separators=(",", ":")).encode("utf-8")
    header = struct.pack(">I", len(data))
    sock.sendall(header + data)


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    chunks = []
    remaining = n
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ProtocolError("Connection closed")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def recv_json(sock: socket.socket, *, max_bytes: int = 1024 * 1024) -> Dict[str, Any]:
    header = _recv_exact(sock, 4)
    (length,) = struct.unpack(">I", header)
    if length <= 0:
        raise ProtocolError("Invalid frame length")
    if length > max_bytes:
        raise ProtocolError(f"Frame too large ({length} > {max_bytes})")

    payload = _recv_exact(sock, length)
    try:
        obj = json.loads(payload.decode("utf-8", errors="strict"))
    except Exception as e:
        raise ProtocolError(f"Invalid JSON: {e}") from None

    if not isinstance(obj, dict):
        raise ProtocolError("Message must be a JSON object")
    return obj


def make_hello(token: Optional[str], client_name: str) -> Dict[str, Any]:
    msg: Dict[str, Any] = {"type": "hello", "proto": PROTO_VERSION, "client": client_name}
    if token is not None:
        msg["token"] = token
    return msg
