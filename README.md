# Command and Control (C2) Server

A basic Command and Control (C2) server implementation using Python's socket module.

## Overview

This script sets up a simple C2 server that listens for incoming connections from clients. It accepts commands from the server operator and sends them to the connected clients, receiving their responses.

## Usage

### Prerequisites

- Python 3.x

### Running the Server

1. Clone the repository or download the script.
2. Open a terminal or command prompt.
3. Run the server script:

```bash
python py_server_c2.py --host <your_host> --port <your_port>
```
```bash
python py_client.py --server-host <server_host> --server-port <server_port>
```

### Interaction

Once the client is connected to the server, it waits for commands. Commands received from the server will be executed in the client's environment. The output of the executed commands is sent back to the server.

# Additional Tools

## HTTPS Banner Retrieval

This Python script retrieves the HTTPS banner of a specified host and port by establishing an SSL/TLS connection using the `ssl` and `socket` modules.

## Description

The script initiates an SSL/TLS connection to the specified host and port using the `ssl.create_default_context()` method and `socket.create_connection()` function. It sends an HTTP GET request to the server and retrieves the banner information.

## Usage

### Prerequisites

- Python 3.x

### Running the Script

1. Clone the repository or download the script.
2. Open a terminal or command prompt.
3. Run the script with the target host and port:

```bash
python py_https_banner.py example.com 443
```



## Disclaimer
This is a basic demonstration and might lack security and advanced features. Use it in controlled environments for educational purposes only.