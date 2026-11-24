#!/usr/bin/env python3
"""Deliver the front page for Tuesday 24 November 2026.

The picture itself was drawn before submission, at build time, and is
committed beside this file as entry.png. At grade time this program
draws nothing: it proves the committed file is a complete, decodable
1024x1024 PNG within the size cap, copies it byte-for-byte to the
output path, and reads the copy back to be sure the bytes survived.

Only the Python standard library is used, so the program runs in the
grader's bare Python 3.13 container with no network.

Usage: python3 main.py [output-path]
The output path is argv[1] when given, else $MAKEFUN_OUTPUT_DIR
joined with entry.png, else /output/entry.png.
"""

import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
PICTURE_PATH = os.path.join(HERE, "entry.png")
BYTE_CAP = 1_048_576
WANTED = (1024, 1024)
SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


class PictureError(Exception):
    """The committed entry.png is not the picture this entry promises."""


def iter_chunks(blob):
    """Walk a PNG's chunks, verifying the CRC of each one.

    Yields (kind, body) pairs in file order. Raises PictureError at
    the first structural defect: bad signature, an overrun, a CRC
    mismatch, or bytes left over after the final chunk.
    """
    if blob[:8] != SIGNATURE:
        raise PictureError("entry.png does not start with the PNG signature")
    pos = 8
    while pos < len(blob):
        if pos + 8 > len(blob):
            raise PictureError("a chunk header runs past the end of the file")
        (length,) = struct.unpack_from(">I", blob, pos)
        kind = blob[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(blob):
            raise PictureError("chunk %r overruns the file" % kind)
        body = blob[pos + 8:pos + 8 + length]
        (stored_crc,) = struct.unpack_from(">I", blob, pos + 8 + length)
        actual_crc = zlib.crc32(kind + body) & 0xFFFFFFFF
        if actual_crc != stored_crc:
            raise PictureError("chunk %r fails its CRC check" % kind)
        yield kind, body
        pos = end


def load_picture(path):
    """Read entry.png and validate it fully; return its raw bytes."""
    with open(path, "rb") as handle:
        blob = handle.read()
    if len(blob) > BYTE_CAP:
        raise PictureError(
            "entry.png is %d bytes, over the %d-byte cap" % (len(blob), BYTE_CAP))
    header = None
    compressed = []
    finished = False
    for kind, body in iter_chunks(blob):
        if finished:
            raise PictureError("chunk %r appears after IEND" % kind)
        if header is None and kind != b"IHDR":
            raise PictureError("the first chunk is %r, not IHDR" % kind)
        if kind == b"IHDR":
            if header is not None:
                raise PictureError("a second IHDR chunk appears")
            header = body
        elif kind == b"IDAT":
            compressed.append(body)
        elif kind == b"IEND":
            if body:
                raise PictureError("the IEND chunk is not empty")
            finished = True
    if header is None:
        raise PictureError("no IHDR chunk: not a readable PNG")
    if not compressed:
        raise PictureError("no IDAT chunk: the PNG carries no image data")
    if not finished:
        raise PictureError("no IEND chunk: the PNG is truncated")
    width, height, depth, colour = struct.unpack(">IIBB", header[:10])
    if (width, height) != WANTED:
        raise PictureError(
            "the image is %dx%d, not %dx%d" % (width, height, *WANTED))
    try:
        raw = zlib.decompress(b"".join(compressed))
    except zlib.error as problem:
        raise PictureError("the IDAT payload does not decompress: %s" % problem)
    if colour not in CHANNELS or depth != 8:
        raise PictureError(
            "unexpected PNG format: colour type %d, bit depth %d" % (colour, depth))
    row_bytes = 1 + width * CHANNELS[colour]
    if len(raw) != row_bytes * height:
        raise PictureError(
            "the decompressed data is %d bytes, not the %d the header "
            "promises" % (len(raw), row_bytes * height))
    return blob


def destination(argv):
    if len(argv) > 1:
        return argv[1]
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.png")
    return "/output/entry.png"


def main(argv):
    try:
        blob = load_picture(PICTURE_PATH)
    except (OSError, PictureError) as problem:
        print("main.py: error: %s" % problem, file=sys.stderr)
        return 1
    target = destination(argv)
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        copied = handle.read()
    digest = hashlib.sha256(blob).hexdigest()
    if hashlib.sha256(copied).hexdigest() != digest:
        print("main.py: error: read-back mismatch at %s" % target, file=sys.stderr)
        return 1
    print("main.py: wrote %s (%d bytes, sha256 %s...)"
          % (target, len(blob), digest[:16]))
    print("main.py: picture is %dx%d, under the %d-byte cap"
          % (WANTED[0], WANTED[1], BYTE_CAP))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
