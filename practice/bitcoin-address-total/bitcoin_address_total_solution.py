"""
You will need to provide your RPC credentials by exporting them to the following
environment variables to prevent accidental upload in solutions:
    $RPC_USER
    $RPC_PASSWORD
"""
from authproxy import AuthServiceProxy
from util import username, password, port

WALLET_NAME = "test-wallet"
ADDRESS = "17rtwA1cKhyAgw9aZceFKBsEdCqqW3ErqC"
ADDRESS_BIRTHDAY = 688393


def get_proxy(username, password, port, wallet=None) -> AuthServiceProxy:
    if wallet:
        # Notice the addition of "/wallet/{wallet_name}" to the URI
        # This query might take a little longer, so increase the timeout
        return AuthServiceProxy(service_url="http://%s:%s@127.0.0.1:%s/wallet/%s" % (username, password, port, WALLET_NAME), timeout=600)
    else:
        return AuthServiceProxy( service_url="http://%s:%s@127.0.0.1:%s" % (username, password, port))


def bitcoin_address_total() -> (int, int):
    """
    :returns    (num_transactions, total_value)
    """
    # Setup the rpc connection
    rpc = get_proxy(username, password, port)

    # Create a wallet called "test-wallet", with "private keys disabled" and "blank"
    rpc.createwallet(WALLET_NAME, True, True)

    # Re-create the rpc object to account for our new wallet
    rpc = get_proxy(username, password, port, WALLET_NAME)

    # Import the chosen address into test-wallet
    # !!! Remember to disable rescan !!!
    rpc.importaddress(ADDRESS, "", False)

    # Choose address "birthday" to rescan from
    rpc.rescanblockchain(ADDRESS_BIRTHDAY)

    # Get all the transactions for the address, send + receive
    transactions = rpc.listtransactions("*", 100)

    # Filter the receives
    receives = [tx["amount"] for tx in transactions if tx["address"] == ADDRESS]

    # Return the result
    return len(receives), sum(receives)
