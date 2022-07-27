# Get Block Header

Foreword: If you are unfamiliar with the mechanics of how bitcoin transactions are added to "blocks", and the blocks are then added to the "blockchain", it would be advisable to follow the hyperlinks in the below text and read the linked paragraphs.

From Mastering Bitcoin, Chapter 2: [How Bitcoin Works](https://github.com/bitcoinbook/bitcoinbook/blob/open_edition/ch02.asciidoc#how-bitcoin-works):

> The bitcoin system, unlike traditional banking and payment systems, is based on decentralized trust. Instead of a central trusted authority, in bitcoin, trust is achieved as an emergent property from the interactions of different participants in the bitcoin system. In this chapter, we will examine bitcoin from a high level by tracking a single transaction through the bitcoin system and watch as it becomes "trusted" and accepted by the bitcoin mechanism of distributed consensus and is finally recorded on the blockchain, the distributed ledger of all transactions. Subsequent chapters will delve into the technology behind transactions, the network, and mining.
> 
> ... the bitcoin system consists of users with wallets containing keys, transactions that are propagated across the network, and miners who produce (through competitive computation) the consensus blockchain, which is the authoritative ledger of all transactions.

When a valid bitcoin transaction is submitted to the network, it will enter the "mempool" waiting to be confirmed. Here is some high level information on the [mining process](https://github.com/bitcoinbook/bitcoinbook/blob/open_edition/ch10.asciidoc#introduction).

In particular, they begin by [aggregating transactions into blocks](https://github.com/bitcoinbook/bitcoinbook/blob/open_edition/ch10.asciidoc#aggregating-transactions-into-blocks) and create a "candidate block" and begin mining with it.
If they are successful with mining, this block and the transactions contained within it will be added to the tip of the blockchain.

Blocks are comprised of two parts:

1. A block header
2. A list of transactions included in the block

The block header contains some vital statistics and takes the following structure (from [bitcoin.it](https://en.bitcoin.it/wiki/Protocol_documentation#Block_Headers)):

|Field Size |Description    |Data type  | Comments  |
| ---       | ---           | ---       | ---       |
| 4         |version	    |int32_t	|Block version information (note, this is signed) |
| 32        |prev_block     |char[32]	|The hash value of the previous block this particular block references |
| 32        |merkle_root    |char[32]	|The reference to a Merkle tree collection which is a hash of all transactions related to this block |
| 4         |timestamp      |uint32_t	|A timestamp recording when this block was created (Will overflow in 2106 [[2](https://en.bitcoin.it/wiki/Protocol_documentation#cite_note-2)]) |
| 4         |bits           |uint32_t	|The calculated difficulty target being used for this block |
| 4         |nonce          |uint32_t	|The nonce used to generate this block… to allow variations of the header and compute different hashes |

The objective of the miner is to repeatedly hash the block header (but not the transactions) until a solution conforming to the current [target](https://en.bitcoin.it/wiki/Target) is found.
Note that the "target" is sometimes talked about in terms of [difficulty](https://en.bitcoin.it/wiki/Difficulty), which is really just a measure of how _difficult_ it is to find a hash below the current target.
Between hashes the miner should slightly tweak some data in the header to incite different outcomes to the hash function.

An in-depth explanation of the mining process can be found in Mastering Bitcoin: Chapter 10 [Mining the Block](https://github.com/bitcoinbook/bitcoinbook/blob/open_edition/ch10.asciidoc#mining-the-block).

Once a solution has been found, the winning miner can distribute their header (and its transactions) to the wider network for validation.
A key point to note here is that, whilst repeatedly hashing block headers to find a "winning" solution is extremely computationally difficult, validating that hash of a single (winning) block header is extremely computationally easy -- it's simply `SHA256(SHA256({block_header}))`.
This means that it takes a lot of (proof of) work to create a valid block, but only a little work to validate one.

The goal of this exercise is to use our Bitcoin Core full node, setup in the _sync-bitcoin-core_ exercise previously, to find the block header of a specific block.

The objectives:

- Connect to a local instance of Bitcoin Core via it's JSON-RPC interface using python.
- Find the block header of block 40,000 of the Signet Blockchain.
- Run the test suite and make sure that it succeeds.
- Submit your solution and check it at the website.

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

To run the tests, run `pytest get_block_header_test.py`

Alternatively, you can tell Python to run the pytest module:
`python -m pytest get_block_header.py`

### Common `pytest` options

- `-v` : enable verbose output
- `-x` : stop running tests on first failure
- `--ff` : run failures from previous test before running other test cases

For other options, see `python -m pytest -h`

## Submitting Exercises

Note that, when trying to submit an exercise, make sure the solution is in the `$EXERCISM_WORKSPACE/python/get-block-header` directory.

You can find your Exercism workspace by running `exercism debug` and looking for the line that starts with `Workspace`.

For more detailed information about running tests, code style and linting,
please see [Running the Tests](http://exercism.io/tracks/python/tests).

## Source

This is an exercise to introduce users to using Exercism [http://en.wikipedia.org/wiki/%22Hello,_world!%22_program](http://en.wikipedia.org/wiki/%22Hello,_world!%22_program)

## Submitting Incomplete Solutions

It's possible to submit an incomplete solution so you can see how others have completed the exercise.
