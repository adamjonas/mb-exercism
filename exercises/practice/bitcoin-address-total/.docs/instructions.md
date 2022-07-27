# Determine how many bitcoin were cumulatively sent to a given address over time.

This is not as easy as it might seem with Bitcoin Core, due to the way the software stores blocks and works with its integrated wallet.
Although every block and transaction is stored on disk, no index is kept of the "balance" of each address, because it's not required for normal wallet operations.

Blocks are store on disk in raw binary form, and Bitcoin Core will retrieve data from them by pointing to the memory address of a particular block or transaction.
i.e. blocks are not stored in a database, but in (roughly) sequential form.
The Bitcoin Core repository contains [linearization tools](https://github.com/bitcoin/bitcoin/tree/0.21/contrib/linearize) which would permit someone to organise the block files *exactly* sequentially on disk, if they required.

So why might this be trickier than we expect?

## UTXO vs account-based systems

Bitcoin is an "UTXO-based" system rather than an "account-based" system.
With an "account-based" system, users have accounts and when a transfer is made one account is debited and one account is credited.
This style of system leads itself to writing software that indexes the blockchain by "account".

With a "UTXO-based" system, like Bitcoin, users do *not* have accounts.
An individual "Unspent Transaction Output" (UTXO) represents a single "coin".
This coin can have variable value -- there are no fixed denominations like physical coins.
It is the job of "wallet software" to collect the sub-set of UTXOs ("coins") which are owned by the user, and display to them an aggregate balance at the current point in time.

Due to this accounting model, unless you are providing wallet services to third party, or performing chain analytics, there is no reason to create an index of the blockchain "by address".

Some more background on the differences between account and UTXO-based models can be found [here](https://academy.glassnode.com/concepts/utxo).

## Indexing by address

This is where so-called "blockchain indexers", like [Electrs](https://github.com/romanz/electrs) and [ElectrumX](https://github.com/spesmilo/electrumx) come in.
These services specialise in indexing the UTXO-based blockchain _by address_ (or more strictly by the `SHA256(scriptPubKey)` -- the so-called `scriptHash`), so that "balances" and transactions "involving this address" can be easily queried by end user wallets.

Naturally it's also possible to construct your own relational database against which you can run queries.

## Manipulating Bitcoin Core wallet logic

It is possible to query Bitcoin Core for a cumulative address balance, but doing so will cost us an entire re-scan of the blockchain.
The reason for this it that we must proceed in the following way in order to leverage Bitcoin Core's wallet logic:

1. Add the address we are interested in to a wallet belonging to us. 
1. Instruct Bitcoin Core to perform a full rescan of the blockchain, looking out for transactions involving this address as it goes.

To avoid a rescan, which can take an hour or longer, we will select an address which was only first used recently and then use the address's "birthday" (in terms of block height) to perform a shorter re-scan; only from the address's "birthday" until the current block at the tip of the chain.

## Exercise objectives

The objectives are:

- Create a new blank "watch-only" wallet called "test-wallet".
- Add the address `17rtwA1cKhyAgw9aZceFKBsEdCqqW3ErqC` to the wallet "test-wallet".
- Instruct core to perform a rescan starting from the block height of the address' birthday: 688393
- Query transactions made involving this address and sum the cumulative received balance.


## Exception messages

Sometimes it is necessary to raise an exception. When you do this, you should include a meaningful error message to
indicate what the source of the error is. This makes your code more readable and helps significantly with debugging. Not
every exercise will require you to raise an exception, but for those that do, the tests will only pass if you include
a message.

To raise a message with an exception, just write it as an argument to the exception type. For example, instead of
`raise Exception`, you should write:

```python
raise Exception("Meaningful message indicating the source of the error")
```

## Running the tests

To run the tests, run `pytest bitcoin_address_total_test.py`

Alternatively, you can tell Python to run the pytest module:
`python -m pytest bitcoin_address_total_test.py`

### Common `pytest` options

- `-v` : enable verbose output
- `-x` : stop running tests on first failure
- `--ff` : run failures from previous test before running other test cases

For other options, see `python -m pytest -h`

## Submitting Exercises

Note that, when trying to submit an exercise, make sure the solution is in the `$EXERCISM_WORKSPACE/python/bitcoin-address-total` directory.

You can find your Exercism workspace by running `exercism debug` and looking for the line that starts with `Workspace`.

For more detailed information about running tests, code style and linting,
please see [Running the Tests](http://exercism.io/tracks/python/tests).

## Source

This is an introduction to performing more complex wallet-specific operations via Bitcoin Core RPC.

## Submitting Incomplete Solutions

It's possible to submit an incomplete solution so you can see how others have completed the exercise.
