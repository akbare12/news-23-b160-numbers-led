#!/usr/bin/env python3
"""THE WORLD TODAY — Monday 23 November 2026 (31 stories), numbers-led.

Validates the bundled entry.png (stdlib only, no PIL) and writes it to
os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png").
Never writes next to main.py: the grader runs this from a read-only copy.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "5cfc4edc357873c453abe49b70274882553899d1bed32dc8aa74e73bf1fdd7de"
EXPECTED_SIZE = 148098
MIN_SIZE = 10000
MAX_SIZE = 1024 * 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def check_png(path):
    """Validate the PNG: signature, IHDR 1024x1024, chunk CRCs, IEND last."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        fail(f"cannot read {path}: {e}")
    if len(data) < MIN_SIZE:
        fail(f"PNG too small: {len(data)} bytes")
    if len(data) > MAX_SIZE:
        fail(f"PNG too large: {len(data)} bytes (> 1 MiB)")
    if data[:8] != PNG_SIG:
        fail("bad PNG signature")
    # First chunk must be a 13-byte IHDR.
    (length,) = struct.unpack(">I", data[8:12])
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        fail("first chunk is not a 13-byte IHDR")
    ihdr = data[16:29]
    width, height, depth, ctype2, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (width, height) != (1024, 1024):
        fail(f"wrong dimensions: {width}x{height} (need 1024x1024)")
    if depth != 8 or ctype2 not in (2, 6):
        fail(f"unsupported IHDR: bit depth {depth}, colour type {ctype2}")
    if comp != 0 or filt != 0 or inter != 0:
        fail("unsupported IHDR: compression/filter/interlace must be 0")
    (crc_stored,) = struct.unpack(">I", data[29:33])
    if zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF != crc_stored:
        fail("CRC mismatch in chunk b'IHDR'")
    # Walk the remaining chunks, checking CRCs; IEND must be last, 0 bytes.
    # NOTE: the CRC covers the chunk type + data (4 + N bytes), NOT the
    # 4-byte length field that precedes them — see PNG spec section 3.2.
    off = 33
    idat_total = 0
    seen_iend = False
    while off < len(data):
        if off + 8 > len(data):
            fail("truncated chunk header")
        (clen,) = struct.unpack(">I", data[off:off + 4])
        ctype = data[off + 4:off + 8]
        if off + 12 + clen > len(data):
            fail(f"truncated chunk {ctype!r}")
        chunk_data = data[off + 8:off + 8 + clen]
        (crc_stored,) = struct.unpack(">I", data[off + 8 + clen:off + 12 + clen])
        if zlib.crc32(ctype + chunk_data) & 0xFFFFFFFF != crc_stored:
            fail(f"CRC mismatch in chunk {ctype!r}")
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND chunk must be 0 bytes")
            if off + 12 + clen != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        off += 12 + clen
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail(f"IDAT payload too small: {idat_total} bytes")
    if len(data) != EXPECTED_SIZE:
        fail(f"size mismatch: {len(data)} != {EXPECTED_SIZE}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        fail("sha256 mismatch")
    return data


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        fail(f"MAKEFUN_OUTPUT_DIR is a file, not a directory: {out_dir}")
    if os.path.commonpath([out_dir_abs, here]) == here:
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("refusing to overwrite the source image")
    data = check_png(src)
    try:
        os.makedirs(out_dir_abs, exist_ok=True)
    except FileExistsError:
        fail(f"MAKEFUN_OUTPUT_DIR is a file, not a directory: {out_dir}")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        fail("output is not byte-identical to the source image")
    print(f"wrote {dst} ({len(data)} bytes, sha256 {hashlib.sha256(back).hexdigest()})")


if __name__ == "__main__":
    main()
