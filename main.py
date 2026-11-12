"""
This script copies art.jpg to a specified output directory and verifies
the copy using a SHA-256 hash comparison.
"""

import os
import hashlib
import sys

def main():
    # Get path to art.jpg in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, 'art.jpg')

    # Get output path from environment or default
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    output_path = os.path.join(output_dir, 'entry.png')

    # Read source bytes
    try:
        with open(source_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find art.jpg at {source_path}", file=sys.stderr)
        sys.exit(1)

    # Check magic bytes for JPEG: FF D8
    if data[:2] != b'\xff\xd8':
        print("Error: Source file art.jpg is not a valid JPEG.", file=sys.stderr)
        sys.exit(1)

    # Create output directory if it does not exist
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Write file
    with open(output_path, 'wb') as f:
        f.write(data)

    # Re-read and check hash
    with open(output_path, 'rb') as f:
        written_data = f.read()

    source_hash = hashlib.sha256(data).hexdigest()
    written_hash = hashlib.sha256(written_data).hexdigest()

    if source_hash != written_hash:
        print("Error: Hash mismatch!", file=sys.stderr)
        sys.exit(1)

    print(f"Output path: {output_path}")
    print(f"Bytes written: {len(data)}")
    print(f"SHA-256 hash: {written_hash}")

if __name__ == "__main__":
    main()
