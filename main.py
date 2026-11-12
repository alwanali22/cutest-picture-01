"""
This program copies the bundled 'art.jpg' picture file to the output location
expected by the competition. It checks that the picture is a valid JPEG
before writing and verifies the written file byte-for-byte afterwards to
ensure integrity.
"""

import os
import sys
import hashlib

# Path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_dir, 'art.jpg')

# Read source
with open(source_path, 'rb') as f:
    source_bytes = f.read()

# JPEG magic check
if source_bytes[:2] != b'\xff\xd8':
    # Need to print a clear error and fail
    print("Error: Not a JPEG file", file=sys.stderr)
    sys.exit(1)

# Determine output path
output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'entry.png')

# Write
with open(output_path, 'wb') as f:
    f.write(source_bytes)

# Re-read and hash
with open(output_path, 'rb') as f:
    written_bytes = f.read()

# Hash verify
source_hash = hashlib.sha256(source_bytes).hexdigest()
written_hash = hashlib.sha256(written_bytes).hexdigest()

if source_hash != written_hash:
    print("Error: Hash mismatch", file=sys.stderr)
    sys.exit(1)

print(f"Output path: {output_path}")
print(f"Bytes written: {len(written_bytes)}")
print(f"SHA-256: {written_hash}")
