import hashlib
import time
import json
import os


def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
            return hashlib.sha256(file_content).hexdigest()
    except (IOError, FileNotFoundError) as e:
        print(f"Error reading file: {e}")
        return None


def save_hash_to_json(file_path, hash_file):
    """Save the hash of a file to a JSON file."""
    file_hash = calculate_file_hash(file_path)
    if file_hash is None:
        return

    # Check if the JSON file exists, otherwise initialize an empty dictionary
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            hashes = json.load(f)
    else:
        hashes = {}

    # Update the JSON data with the new hash
    hashes[file_path] = file_hash
    with open(hash_file, "w") as f:
        json.dump(hashes, f, indent=4)
    print(f"Hash saved for {file_path}: {file_hash}")


def detect_file_changes(file_path, hash_file):
    """Detect changes in a file based on its hash stored in a JSON file."""
    # Load the stored hashes
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            hashes = json.load(f)
    else:
        hashes = {}

    # Get the last stored hash
    last_hash = hashes.get(file_path)
    print(f"Initial hash from JSON: {last_hash}")

    while True:
        current_hash = calculate_file_hash(file_path)
        print(f"Current hash: {current_hash}")

        if current_hash != last_hash:
            print("File has changed!")
            save_hash_to_json(file_path, hash_file)
            break

        time.sleep(1)


if __name__ == "__main__":
    hash_file_path = "file_hashes.json"
    file_to_monitor = "testing_files/sample.md"

    # Save initial hash if it doesn't exist in the JSON
    save_hash_to_json(file_to_monitor, hash_file_path)

    # Start monitoring for changes
    detect_file_changes(file_to_monitor, hash_file_path)


## not desired outcome
# program starts > file is being read > if file is modified DURING program runtime 
# > change is caught and program stops
# however now saves in json file
