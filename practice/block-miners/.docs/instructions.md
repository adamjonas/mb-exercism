# Analyze Block Miners

This exercise will have the student analyse the blockchain for data that miners can choose to add to the blocks that they mine.

## Concepts

Terms we will become familiar with in this exercise:

Bitcoin:

* blocks
* block reward (aka coinbase reward)
* candidate block
* coinbase (aka coinbase data)
* difficulty target
* extra nonce
* input
* merkle root
* merkle tree
* miner
* mining reward
* SHA256
* transaction

RDB:

* SQL
* PostgreSQL

## Background

To begin, student should familiarise themselves with the section on [mining nodes][mining nodes] in the Bitcoin Book.
Miners are free to add any valid transactions to the block that they like, but they are unable to modify transactions to add or remove any data to them.
When miners 

This exercise involves looking at the [Coinbase transaction](https://en.bitcoin.it/wiki/Coinbase), which is the transaction a miner uses to reward themselves with new coins according to Bitcoin's reward schedule.
Inside this transaction, in the input section, miners are free to write a short message, and often miners will choose this area to advertise which miner or pool they identify with.
This information can therefore be used to infer (but not prove) which miners mined which blocks.
Note that it is costless to spoof the information in this field and miners are freely able to do so.
This information is not indexed and readily available natively from the Blockchain as stored on disk by Bitcoin Core.

At this point we could choose from two methods of gathering the data:

1. Query Bitcoin Core for each block, save the data we are interested in only.
2. Query Bitcoin Core for each block, save all block data to a relational database for reuse.

We are going to follow path 2, as this will let us re-use the data in future exercises.

## Relational Database

We are going to use PostgreSQL because it is fast, free and open-source (FOSS).
Whilst it is tempting (and possible) to use the simpler sqlite via Python's built-in `sqlite3` module, Postgres should yield us better results in future exercises and allow us to store arrays with ease. 

In order to use Postgres you will first need to install the database component from the [Postgres homepage](https://www.postgresql.org/download/).
Once Postgres is downloaded and installed, it has likely been autostarted.
To see if Postgres is running, you can follow the steps at the [createdb](https://www.postgresql.org/docs/13/tutorial-createdb.html) page of the Postgres user guide to see if you can create a new database.

If Postgres is running, you are ready to move on to manipulating the database with Python.

## psycopg2

In order to talk to our Postgres database we need an adapter (driver) so that our Python program can talk to the database.
Psycopg2 is a fully-featured, [PEP-249](https://www.python.org/dev/peps/pep-0249/) compliant driver for Postgres.


## Bitcoin bits

We are going to take a look at which miners mined each block, by viewing (falsifiable) information stored in the Coinbase Input.

[mining nodes]: https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch10.asciidoc#mining-nodes
