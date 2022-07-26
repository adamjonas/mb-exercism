TABLE_BLOCKS = '''
CREATE TABLE IF NOT EXISTS blocks (
    hash                varchar    primary key,
    confirmations       integer,
    height              integer,
    size                integer,
    strippedsize        integer,
    weight              integer,
    version             integer,
    versionHex          varchar,
    merkleroot          varchar,
    tx                  varchar[],
    time                integer,
    mediantime          integer,
    nonce               integer,
    bits                varchar,
    difficulty          numeric,
    chainwork           varchar,
    nTx                 integer,
    previousblockhash   varchar,
    nextblockhash       varchar
    );
'''

TABLE_TX = '''
CREATE TABLE IF NOT EXISTS transactions (
    hex             varchar,
    txid            varchar     primary key,
    hash            varchar,
    size            integer,
    vsize           integer,
    weight          integer,
    version         integer,
    locktime        integer,
    vin             varchar[],
    vout            varchar[],
    blockhash       varchar,
    confirmations   integer,
    blocktime       integer,
    time            integer
    );
'''

TABLE_VIN = '''
CREATE TABLE IF NOT EXISTS vin (
    txid        varchar primary key,
    vout        varchar,
    scriptsig   varchar,
    sequence    integer
    );
'''

TABLE_VOUT = '''
CREATE TABLE IF NOT EXISTS vout (
     txid        varchar primary key,
     vout        varchar,
     scriptsig   varchar,
     sequence    integer
     );
'''

ROW_BLOCK = '''
INSERT INTO blocks (hash, confirmations, height, size, strippedsize, weight, version, versionHex, merkleroot, tx, time, mediantime, nonce, bits, difficulty, chainwork, nTx, previousblockhash, nextblockhash ) 
VALUES (%(hash)s, %(confirmations)s, %(height)s, %(size)s, %(strippedsize)s, %(weight)s, %(version)s, %(versionHex)s, %(merkleroot)s, %(tx)s, %(time)s, %(mediantime)s, %(nonce)s, %(bits)s, %(difficulty)s, %(chainwork)s, %(nTx)s, %(previousblockhash)s, %(nextblockhash)s);
'''

ROW_GENESIS_BLOCK = '''
INSERT INTO blocks (hash, confirmations, height, size, strippedsize, weight, version, versionHex, merkleroot, tx, time, mediantime, nonce, bits, difficulty, chainwork, nTx, previousblockhash, nextblockhash ) 
VALUES (%(hash)s, %(confirmations)s, %(height)s, %(size)s, %(strippedsize)s, %(weight)s, %(version)s, %(versionHex)s, %(merkleroot)s, %(tx)s, %(time)s, %(mediantime)s, %(nonce)s, %(bits)s, %(difficulty)s, %(chainwork)s, %(nTx)s, %(previousblockhash)s, %(nextblockhash)s);
'''