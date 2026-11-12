"""
This module reads 'art.jpg' from the same directory, verifies it is a JPEG,
and writes it to the output directory defined by MAKEFUN_OUTPUT_DIR.
"""
import os
import sys
import hashlib

# Paths
source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art.jpg")
output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
output_path = os.path.join(output_dir, "entry.png")

# 1. Read source
try:
    with open(source_path, "rb") as f:
        data = f.read()
except FileNotFoundError:
    print(f"Error: {source_path} not found.")
    sys.exit(1)

# 2. Check JPEG magic bytes
if len(data) < 2 or data[:2] != b'\xff\xd8':
    print("Error: Not a JPEG file.")
    sys.exit(1)

# 3. Create output dir
os.makedirs(output_dir, exist_ok=True)

# 4. Write to output
with open(output_path, "wb") as f:
    f.write(data)

# 5. Re-read and check hash
with open(output_path, "rb") as f:
    written_data = f.read()

source_hash = hashlib.sha256(data).hexdigest()
written_hash = hashlib.sha256(written_data).hexdigest()

if source_hash != written_hash:
    print("Error: Hash mismatch.")
    sys.exit(1)

# 6. Print info
print(f"Path: {output_path}")
print(f"Size: {len(written_data)} bytes")
print(f"SHA-256: {written_hash}")
