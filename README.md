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
python c2_server.py --host <your_host> --port <your_port>
```
```bash
python c2_client.py --server-host <server_host> --server-port <server_port>
```

### Interactiob

Once the client is connected to the server, it waits for commands. Commands received from the server will be executed in the client's environment. The output of the executed commands is sent back to the server.

## Disclaimer
This is a basic demonstration and might lack security and advanced features. Use it in controlled environments for educational purposes only.