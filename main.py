#!/usr/bin/env python3
"""make.fun entrypoint for news-image-20261121 (v2).

Validates entry.png (which lives next to this file) as a well-formed
PNG within the competition limits, then copies it byte-for-byte to
the output directory as entry.png.

Validation (standard library only):
  * file size at most 1 MiB (1048576 bytes)
  * PNG signature present
  * chunk stream parses; every chunk's CRC32 (over type + data) matches
  * first chunk is IHDR; width and height at most 1024 px
  * an IEND chunk is present

Output directory: $MAKEFUN_OUTPUT_DIR if set, else /output if it
exists, else ./out next to this file. The directory is created if
needed. The copy is byte-for-byte: the file is read and written in
binary mode with no re-encoding, so repeated runs are identical.
"""

import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

MAX_BYTES = 1048576
MAX_DIM = 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def validate_png(data):
    """Raise ValueError if data is not a valid, in-limits PNG."""
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if not data.startswith(PNG_SIG):
        raise ValueError("entry.png does not start with the PNG signature")

    pos = len(PNG_SIG)
    seen_ihdr = False
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length
        if end + 4 > len(data):
            raise ValueError(f"truncated chunk {ctype!r}")
        cdata = data[pos + 8:end]
        (crc_stored,) = struct.unpack(">I", data[end:end + 4])
        crc_actual = zlib.crc32(ctype + cdata) & 0xFFFFFFFF
        if crc_actual != crc_stored:
            raise ValueError(f"CRC mismatch in chunk {ctype!r}")
        if not seen_ihdr:
            if ctype != b"IHDR":
                raise ValueError("first chunk is not IHDR")
            width, height = struct.unpack(">II", cdata[:8])
            if width > MAX_DIM or height > MAX_DIM:
                raise ValueError(f"image is {width}x{height}, over 1024x1024")
            seen_ihdr = True
        if ctype == b"IEND":
            seen_iend = True
            pos = end + 4
            break
        pos = end + 4

    if not seen_ihdr:
        raise ValueError("no IHDR chunk found")
    if not seen_iend:
        raise ValueError("no IEND chunk found")


def output_dir():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(HERE, "out")


def main():
    with open(SRC, "rb") as fh:
        data = fh.read()
    validate_png(data)
    outdir = output_dir()
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
    print(f"OK: copied {len(data)} bytes -> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
