import os

# Get environment variables
username = os.environ.get("RPC_USER")
password = os.environ.get("RPC_PASSWORD")
port = os.environ.get("RPC_PORT", "8332")
if not username:
    raise Exception("Can't find $RPC_USER environment variable")
if not password:
    raise Exception("Can't find $RPC_PASSWORD environment variable")