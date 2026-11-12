"""
This module reads an art.jpg file, validates its format, and copies it to a
specified output directory while ensuring the integrity of the file by
verifying both its size and SHA-256 hash.
"""
import os
import sys
import hashlib
import shutil

def get_sha256(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def main():
    art_path = os.path.join(os.path.dirname(__file__), 'art.jpg')
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    target_path = os.path.join(out_dir, 'entry.png')

    # Validate art.jpg
    if not os.path.exists(art_path):
        print(f"Error: {art_path} not found.")
        sys.exit(1)

    with open(art_path, 'rb') as f:
        magic = f.read(3)
        if magic != b'\xff\xd8\xff':
            print("Error: art.jpg is not a valid JPEG.")
            sys.exit(1)

    # Copy to target
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(art_path, target_path)

    # Verify
    art_size = os.path.getsize(art_path)
    target_size = os.path.getsize(target_path)

    if art_size != target_size:
        print(f"Error: Size mismatch (art: {art_size}, target: {target_size})")
        sys.exit(1)

    art_hash = get_sha256(art_path)
    target_hash = get_sha256(target_path)

    if art_hash != target_hash:
        print(f"Error: Hash mismatch (art: {art_hash}, target: {target_hash})")
        sys.exit(1)

    print(f"Success! Output: {target_path}, Size: {target_size} bytes, SHA-256: {target_hash}")

if __name__ == '__main__':
    main()
