import socket
import subprocess
import webbrowser
import time
import os
import sys

def find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to venv python
venv_python = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")

if not os.path.exists(venv_python):
    print("Virtual environment not found!")
    sys.exit(1)

port = find_free_port()

# Start waitress using venv python
process = subprocess.Popen([
    venv_python,
    "-m",
    "waitress",
    "--listen=127.0.0.1:" + str(port),
    "dpl_core.wsgi:application"
], cwd=BASE_DIR)

# Wait for server to start
time.sleep(3)

webbrowser.open(f"http://127.0.0.1:{port}")