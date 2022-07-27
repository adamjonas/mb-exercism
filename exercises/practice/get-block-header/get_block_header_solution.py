"""
Before beginning, ensure that you have Bitcoin Core installed and running.

In addition, the RPC Server needs to be enabled as detailed in [sync-bitcoin-core]
exercise.

You will need to provide your RPC credentials by exporting them to the following
environment variables to prevent accidental upload in solutions:
    $RPC_USER
    $RPC_PASSWORD
"""

from authproxy import AuthServiceProxy
from util import username, password, port


def get_proxy(rpc_user, rpc_password, rpc_port) -> AuthServiceProxy:
    return AuthServiceProxy(service_url="http://%s:%s@127.0.0.1:%s" % (rpc_user, rpc_password, rpc_port))


def get_block_header(height: int) -> str:
    """This function should return a hex string of the block header.
    Hint: It will take two RPC calls minimum.
    """

    rpc = get_proxy(username, password, port)
    header_hash = rpc.getblockhash(height)
    header = rpc.getblockheader(header_hash, False)
    return header
