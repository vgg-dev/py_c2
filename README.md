<p align="center">
  <img src="c2_icon.png" alt="py_c2" width="180" height="180" />
</p>

<h1 align="center">py_c2</h1>
<p align="center">A tiny Python socket-based client/server command channel for <b>local lab / educational</b> use.</p>

<p align="center">
  <a href="https://github.com/vgg-dev/py_c2">
    <img alt="repo" src="https://img.shields.io/badge/github-vgg--dev%2Fpy__c2-111827" />
  </a>
  <a href="LICENSE">
    <img alt="license" src="https://img.shields.io/github/license/vgg-dev/py_c2" />
  </a>
  <img alt="python" src="https://img.shields.io/badge/python-3.x-blue" />
  <a href="https://github.com/vgg-dev/py_c2/commits/main">
    <img alt="last commit" src="https://img.shields.io/github/last-commit/vgg-dev/py_c2" />
  </a>
</p>

> [!IMPORTANT]
> **Authorized use only.** This repo demonstrates a basic remote command channel where the client executes commands received from the server and returns output.
>
> It is intentionally minimal and **not secure** (no authentication, no encryption, no hardening). Run only in a controlled environment (e.g., localhost, lab VM network).

## ✨ What’s in this repo

- `py_server_c2.py` — simple TCP server that accepts a client and sends operator-entered commands
- `py_client.py` — simple TCP client that connects and executes received commands
- `py_https_banner.py` — small helper that fetches an HTTPS banner via TLS + a basic HTTP request

## 🧭 Architecture (high level)

```mermaid
flowchart LR
  op["Operator\n(terminal)"] -->|"types command"| srv["py_server_c2.py\nTCP server"]
  srv -->|"command"| cli["py_client.py\nTCP client"]
  cli -->|"stdout/stderr"| srv
  srv -->|"prints result"| op
```

## 🚀 Quickstart (lab only)

### Prerequisites

- Python 3.x

### Run the server

```bash
python py_server_c2.py --host 127.0.0.1 --port 4444
```

### Run the client

In a second terminal:

```bash
python py_client.py --server-host 127.0.0.1 --server-port 4444
```

### Interaction

- Server: type a command and press Enter
- Client: executes the command in its environment and sends output back

## 🧰 HTTPS banner tool

Fetch a simple HTTPS banner for a host/port:

```bash
python py_https_banner.py example.com 443
```

## 🔐 Security notes

This project is a minimal demo and omits common safety/security controls, including:

- Authentication and authorization
- Transport encryption
- Input validation / command restrictions
- Auditing, logging, and tamper resistance

If you extend this for legitimate internal tooling, consider adding mutual authentication (e.g., mTLS), strict allowlists, and limiting the command surface.

## 📄 License

See `LICENSE`.
