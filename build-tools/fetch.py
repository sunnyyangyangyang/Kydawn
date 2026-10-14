#!/usr/bin/env python3
"""Fetch build tools from the network per manifest.tsv and verify sha256.

Cross-platform (Linux/Windows, python3). No third-party deps.
Each manifest line: dest<TAB>url<TAB>sha256-of-download<TAB>zip-member (optional).
"""
import hashlib
import os
import shutil
import sys
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = os.getcwd()
    cache = {}
    with open(os.path.join(HERE, "manifest.tsv"), encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    for line in lines:
        parts = line.split("\t")
        if len(parts) < 3:
            sys.exit(f"bad manifest line: {line!r}")
        dest, url, want = parts[0], parts[1], parts[2]
        member = parts[3].strip() if len(parts) > 3 and parts[3].strip() else None
        dest = os.path.join(root, dest)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if url not in cache:
            tmp = os.path.join(root, ".fetch-" + os.path.basename(dest) + ".part")
            print(f"[fetch] {url}")
            try:
                urllib.request.urlretrieve(url, tmp)
            except Exception as e:
                sys.exit(f"download failed: {url}: {e}")
            got = sha256_of(tmp)
            print(f"[sha256] {got}")
            if got != want:
                sys.exit(f"sha256 mismatch for {url}: {got} != {want}")
            cache[url] = tmp
        tmp = cache[url]
        if member:
            with zipfile.ZipFile(tmp) as z:
                extracted = z.extract(member, root)
            shutil.copyfile(extracted, dest)
            os.remove(extracted)
        else:
            shutil.copyfile(tmp, dest)
        print(f"[ok] {dest}")
    for tmp in cache.values():
        os.remove(tmp)
    print("all build tools fetched and verified")


if __name__ == "__main__":
    main()
