"""
You will need to provide your RPC credentials by exporting them to the following
environment variables to prevent accidental upload in solutions:
    $RPC_USER
    $RPC_PASSWORD
"""
import psycopg2
from typing import List

from authproxy import AuthServiceProxy
from sql import TABLE_BLOCKS, TABLE_TX, TABLE_VIN, TABLE_VOUT, ROW_BLOCK, ROW_GENESIS_BLOCK
from util import username, password, port


def get_blocks(start: int, stop: int) -> List[dict]:
    """
    Fetch blocks via Bitcoind JSON-RPC
    :param start: block height
    :param stop: block height
    :return: list of Blocks
    """
    rpc = AuthServiceProxy(service_url="http://%s:%s@127.0.0.1:%s" % (username, password, port))
    blocks = []
    for i in range(start, stop):
        block = rpc.getblock(rpc.getblockhash(i), 1)
        blocks.append(block)
    return blocks


def db_connect() -> psycopg2._psycopg.connection:
    """
    Connect to a database
    :return: psycopg2 connection
    """
    try:
        conn = psycopg2.connect(database="postgres", user="will", password="", host="127.0.0.1", port="5432")
        print("Database opened successfully")
    except psycopg2.Error as e:
        raise e
    return conn


def db_create_tables(conn: psycopg2._psycopg.connection):
    """
    Create tables with pre-determined rows if missing
    Does not commit
    :param cur: the psycopg2 database connection
    """
    with conn.cursor() as cur:
        cur.execute(TABLE_BLOCKS)
        cur.execute(TABLE_TX)
        cur.execute(TABLE_VIN)
        cur.execute(TABLE_VOUT)


def _db_list_tables(conn: psycopg2._psycopg.connection):
    """
    Helper function to test db connection by listing active tables
    :param conn:
    :return:
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """)
        for table in cur.fetchall():
            print(table)


def _db_danger_delete_table(conn: psycopg2._psycopg.connection, table: str):
    """
    Delete a table.
    Does not commit
    :param conn:
    :param table:
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            DROP TABLE IF EXISTS %s
            """ % table)


def db_insert_block(cur: psycopg2._psycopg.cursor, block: dict):
    """
    Inserts a new block into the table named "blocks".
    Does not commit.
    :param cur: psycopg2._psycopg.cursor
    :param block: block dict as returned by Bitcoin RPC
    """
    cur.execute(ROW_BLOCK, block)


def db_insert_genesis_block(cur: psycopg2._psycopg.cursor, block: dict):
    """
    Inserts a genesis block into the table named "blocks".
    Does not commit the result so that commits can be batched.
    :param cur: psycopg2._psycopg.cursor
    :param block: block dict as returned by Bitcoin RPC
    """
    cur.execute(ROW_GENESIS_BLOCK, block)


def db_get_best_block(conn: psycopg2._psycopg.connection):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT MAX(height)
            FROM blocks
            """
        )
        return cur.fetchone()


if __name__ == "__main__":
    # Connect to the db
    conn = db_connect()

    # Create table if missing
    db_create_tables(conn)
    conn.commit()

    # Setup RPC
    rpc = AuthServiceProxy(service_url="http://%s:%s@127.0.0.1:%s" % (username, password, port))

    # Get current blockheight
    height = rpc.getblockchaininfo()["blocks"]

    # TODO: Check best block height in table
    best_block = db_get_best_block(conn)[0]

    # Fetch, insert and commit blocks to the db in batches of 2000
    BATCH = 2000
    start = 0 if not best_block else best_block + 1
    end = height
    for i in range(start, end, BATCH):
        _start = i
        _end = min(end, i+BATCH-1)
        blocks = get_blocks(_start, _end)
        with conn.cursor() as cur:
            for block in blocks:
                try:
                    if block.get("height") == 0:
                        db_insert_genesis_block(cur, block)
                    else:
                        db_insert_block(cur, block)
                except psycopg2.Error as e:
                    print(e)
                    print(f"Stopping db update without committing blocks {_start} to {_end}")
                    break
            conn.commit()
            print(f"Added blocks {_start} to {_end}")

    # Get coinbase transactions


    conn.close()
