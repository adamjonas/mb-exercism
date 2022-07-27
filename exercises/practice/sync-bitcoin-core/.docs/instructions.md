# Sync Bitcoin Core

This is an introductory exercise to get Bitcoin Core installed and running on your machine.

The objectives are as follows:

- Download Bitcoin Core.
- (optional, recommended) Verify the signature and checksum of the pre-compiled binary.
- Install Bitcoin Core.
- Run Bitcoin Core connected to the [Signet](https://en.bitcoin.it/wiki/Signet) test network.
- Enable the RPC server.

Bitcoin Core is the reference node implementation for the Bitcoin cryptocurrency network written in C++.
It includes the following key components:

|Component | Function |
| --- | --- |
| Peer to Peer (P2P) network stack | Communication with peers over IP, Tor, I2P. |
| Consensus engine | Verify transactions and blocks cryptographically, and according to Bitcoin protocol. |
| Database stack | Store historical blocks and the current UTXO set. |
| Mempool | Store valid but unconfirmed transactions. |
| Wallet | Create and sign bitcoin transactions, and store cryptographic keys and bitcoin scripts. |
| RPC server | Remote control of Bitcoin Core by other programs. |
| `bitcoin-cli` tool | Control Bitcoin Core from the command line. |
| Miner | Construct valid blocks from transactions in the mempool, for mining. |
| Graphical User Interface | `bitcoin-qt` is a [QT](https://www.qt.io)-based GUI for Bitcoin Core |

A peer on the Bitcoin network who is using their own node to validate incoming transactions can be sure that coins they receive adhere to the rules of the network, without having to trust any third party.
This ability is paramount to the self-sovereign, decentralised nature of Bitcoin, so running your own node is strongly advised where possible.

In addition to this, using the RPC server (or the `bitcoin-cli` tool) allows you to execute Bitcoin transactions, using well-reviewed cryptography and wallet code.

Finally, because a full copy of the blockchain is stored locally, some basic blockchain and transaction analysis are possible.
For more advanced analysis, construction of a relational database from your local copy of the blockchain will yield better performance than using Bitcoin Core's block storage structure via RPCs.

## 1. Download Bitcoin Core 

Download the appropriate pre-compiled binary for your operating system from: https://bitcoincore.org/en/download/

## 2. (optional): Install gpg and verify GPG signature for Bitcoin Core binary

- Linux: Install [gpg](https://gnupg.org/download/) using your system package manager, if not already installed
- MacOS: Install [GPGTools](https://gpgtools.org)
- Windows: Install [Gpg4win](https://gpg4win.org/download.html)

Open a new Terminal window and add the Bitcoin Core signing key, `01EA5486DE18A882D4C2684590C8019E36C2E964` by running command:

```bash
gpg --receive-keys 01EA5486DE18A882D4C2684590C8019E36C2E964
```

Follow the instructions under heading “Verify your download” on page: https://bitcoincore.org/en/download/ to use GPG to verify the binary has been signed by the Bitcoin Core organisation’s signing key.

You do not need to complete the instructions underneath heading “Additional verification with reproducible builds”

## 3. Install Bitcoin Core using the downloaded binary

- [Linux instructions](https://bitcoin.org/en/full-node#linux-instructions)
- [MacOS instructions](https://bitcoin.org/en/full-node#mac-os-x-instructions)
- [Windows instructions](https://bitcoin.org/en/full-node#windows-instructions)

## 4. Enable the RPC server and connect to Signet

If we want to control Bitcoin Core from another program then we need to enable the [JSON-RPC server](https://github.com/bitcoin/bitcoin/blob/master/doc/JSON-RPC-interface.md).
The RPC server is disabled by default for `bitcoin-qt` and is enabled by default for `bitcoind`.

Steps:

- Generate a secure set of RPC user credentials
- Update `bitcoin.conf` file:
  - enable RPC server 
  - add RPC credentials
  - enable Signet

### Generate RPC credentials using rpc_auth.py

So that you don't have to store your RPC password in plaintext (in the `bitcoin.conf` configuration file) Bitcoin Core accepts a special `rpcauth=...` string which comprises the RPC username, a salt, and an HMAC derived from the password.

This obfuscated string is stored in your configuration file, and when you want to issue an RPC from another program you provide the username and password.

To generate the `rpcauth=` string run the included file `rpc_auth.py` in your Terminal, passing it one argument: `{rpc_username}`:

```bash
$ rpc_auth.py {your_username}
```

This will print out two items to the terminal in the following form:

```text
String to be appended to bitcoin.conf:
rpcauth={your_username}:{salt + HMAC}
Your password:
{your_unique_random_password}
```

Keep the password safe for the remainder of the course -- we'll use it regularly. You might want to consider using a Password Manager to keep it safe.

The `rpcauth=...` string just needs to be kept until the next step when we add it to our config file, after that we don't need a physical backup. We can always regenerate a new line for the config file if necessary.

The `rpc_auth.py` file is directly copied from the main Bitcoin Core code repository from the [bitcoin/share](https://github.com/bitcoin/bitcoin/blob/0.21/share/rpcauth/rpcauth.py) directory.

### Update `bitcoin.conf`

We are going to add the settings to `bitcoin.conf`. This file, which may not exist yet if this is the first time you've ever run Bitcoin Core, is stored in Bitcoin's "datadir" (data directory), whose location varies by platform:

- [Linux](https://en.bitcoin.it/wiki/Data_directory#Linux)
- [MacOS](https://en.bitcoin.it/wiki/Data_directory#Mac)
- [Windows](https://en.bitcoin.it/wiki/Data_directory#Windows)

Navigate to the Bitcoin datadir for your OS and (create if necessary and) edit the file `bitcoin.conf` by adding and then amending the following lines:

```text
server=1    # enable RPC server
signet=1    # enable Signet mode
rpcauth=... # This is the string we generated using rpc_auth.py
```

In order for the settings to take effect we must restart any running clients.

## 5. Run Bitcoin Core GUI

### Linux / MacOS

Open a terminal and run:

```bash
# Start Bitcoin Core GUI
bitcoin-qt
```

If your terminal cannot find the `bitcoin-qt` command, check that the installation directory is in your systems "PATH" environment variable.

### Windows

Open the Start Menu and start typing "bitcoin", clicking the icon when it appears to start the program.

### Syncing the Bitcoin Signet blockchain

Syncing Signet Blockchain will require approximately 120 MB of download bandwidth as well as storage space.

If Bitcoin Core is running on your machine, then it will already be automatically starting the syncing process with the rest of the network.

First it tries to find out the IP addresses of other nodes on the network, so that it can request blocks and other data from them.
It tries to this by executing the following logic:

1. If any node IP addresses were passed to the process (or set in `bitcoin.conf`) using the `--addnode`, `--seednode` or `--connect` options, it will try to connect to these nodes, request more node IP addresses optionally disconnect from the nodes added via configuration options.
2. If no nodes were passed to the process, it will contact a [list](https://github.com/bitcoin/bitcoin/blob/0.21/src/chainparams.cpp#L123-L131) of [DNS seeds](https://github.com/bitcoin/bitcoin/blob/7fcf53f7b4524572d1d0c9a5fdc388e87eb02416/doc/dnsseed-policy.md) to request node IP addresses and disconnect from the DNS seeder.
3. If it cannot connect to the DNS seeds it will attempt to connect to nodes directly from its list of [hardcoded seeds](https://github.com/bitcoin/bitcoin/blob/0.21/contrib/seeds/nodes_main.txt), request more node IP addresses and disconnect from the hardcoded seeds.

The client will request new addresses from connected nodes in methods 1) and 3) by sending [getaddr](https://developer.bitcoin.org/reference/p2p_networking.html#getaddr) messages and waiting for [addr](https://developer.bitcoin.org/reference/p2p_networking.html#addr) responses.
The DNS seeders in method 2) return addresses in the `ANSWER` section of a DNS query (you can try for yourself, in a Terminal: `dig seed.bitcoin.sipa.be`). 

In the event that the client cannot make any connections using any of the above methods, this indicates a wider networking issue e.g. with the machine's firewall or the network's router.

## 6. Confirm that RPC server is running

You can check that the RPC server is running from within Bitcoin Core GUI:

- First, click the "Window" menu and choose "Information".
- Next click "Open" next to 'Debug log file' to open the debug log.
- Look for lines containing the following:
    - `Config file arg: server="1"`
    - `Config file arg: rpcauth=****`
- If you'd like to run a test command to confirm it's working, open a new Terminal window and run:
    - `bitcoin-cli -signet getnetworkinfo`
    - This should print a list of statistics about the nodes' network connections

Note that we did not need to provide RPC username and password to the `bitcoin-cli` tool, this is because Bitcoin Core generates a magic `.cookie` file which provides RPC authentication for programs running on the same machine as the same user.

## Running the tests

There are no tests to be run for this exercise, congratulations if you got Bitcoin Core up and running!

## Submitting Exercises

There is no submission required for this exercise. If you had any difficulty with installing or running Bitcoin Core on your machine:

TODO: get in contact?

## Source

This is an exercise to introduce users to [Bitcoin Core](https://github.com/bitcoin/bitcoin).

You can find more in depth information on Bitcoin Core in "Mastering Bitcoin" Chapter 3: [Bitcoin Core: The Reference Implementation](https://github.com/bitcoinbook/bitcoinbook/blob/open_edition/ch03.asciidoc).

## Submitting Incomplete Solutions

There are no incomplete solutions to submit for this exercise.

## TODOs

[//]: # Should we have them clone the main repo and build from source?

[//]: # How well should we cater to Windows users? I have assumed equally to Linux/MacOS as a default.
