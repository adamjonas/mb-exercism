import struct
from decimal import Decimal
from typing import List

from binascii import unhexlify
from dataclasses import dataclass, field


@dataclass
class CBlock:
    hash: str = ""
    confirmations: int = 0
    size: int = 0
    strippedsize: int = 0
    weight: int = 0
    version: int = 2
    versionHex: str = 32*b'00'
    merkleroot: str = 32*b'00'
    tx: List[str] = field(default_factory=list)
    time: int = 0
    mediantime: int = 0
    nonce: int = 0
    bits: str = ""
    difficulty: Decimal = Decimal('0.0')
    chainwork: str = ""
    nTx: int = 0
    previousblockhash: str = ""
    nextblockhash: str = ""

    @classmethod
    def from_dict(cls, header: dict):
        for key in header:
            setattr(cls, key, header[key])
        return cls


@dataclass
class BlockHeader:
    """
    Represents a Bitcoin Block Header
    """
    version: str        # int32, 4 bytes, le
    prev_block: str     # 32 bytes
    merkle_root: str    # 32 bytes
    time: int           # uint32, 4 bytes, le
    bits: int           # uint32, 4 bytes, le
    nonce: int          # uint32, 4 bytes, le

    @classmethod
    def deserialize(cls, header_hex: str):
        header_bytes = unhexlify(header_hex)
        version = struct.unpack("<i", header_bytes[0:4])[0]
        hash_prev_block = struct.unpack("32s", header_bytes[4:36])[0]
        hash_merkle_root = struct.unpack("32s", header_bytes[36:68])[0]
        time = struct.unpack("<I", header_bytes[68:72])[0]
        bits = struct.unpack("<I", header_bytes[72:76])[0]
        nonce = struct.unpack("<I", header_bytes[76:80])[0]
        return cls(version, hash_prev_block, hash_merkle_root, time, bits, nonce)


# def deser_headers(headers: List[str]) -> List[BlockHeader]:
#     """
#     Deserialise hex-encoded block headers into their constituent values
#     :param headers: list of hex-encoded Block Headers
#     :return: list of BlockHeaders
#     """
#     _headers = []
#     for header in headers:
#         _headers.append(BlockHeader.deserialize(header))
#     return _headers
