import hashlib
import time

def calculate_file_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            file_content = f.read() # debug
            print(f"File content: {file_content[:50]}...") # debug
            return hashlib.sha256(file_content).hexdigest()
    except (IOError, FileNotFoundError) as e:
        print(f"Error reading file: {e}")
        return None



def detect_file_changes(file_path):
    last_hash = calculate_file_hash(file_path)
    print(f"Initial hash: {last_hash}") # debug
    while True:
        current_hash = calculate_file_hash(file_path)
        print(f"Current hash: {current_hash}") # debug
        if current_hash != last_hash:
            print("File has changed!")
            break
        time.sleep(1)


if __name__ == "__main__":
    detect_file_changes("testing_files/sample.md")

## not desired outcome
# program starts > file is being read > if file is modified DURING program runtime 
# > change is caught and program stops

"""
File content: b'### Hello\r\n123\r\n144111'...
Current hash: 1fca468f66790a97d2b6bc743421a4c9cf3be4f6e96499a97c0bf1314a069ada
File content: b'### Hello\r\n123\r\n144111'...
Current hash: 1fca468f66790a97d2b6bc743421a4c9cf3be4f6e96499a97c0bf1314a069ada
File content: b'### Hello\r\n123\r\n144111'...
Current hash: 1fca468f66790a97d2b6bc743421a4c9cf3be4f6e96499a97c0bf1314a069ada
File content: b'### Hello\r\n123\r\n144111'...
Current hash: 1fca468f66790a97d2b6bc743421a4c9cf3be4f6e96499a97c0bf1314a069ada
File content: b'### Hello\r\n123\r\n144111asdf'...
Current hash: f34a90124bf03ca728858943d877d75ae8b6df202bfece931df033fce1224452
File has changed!
"""

## save files' instances in .json file, check subsequent file hashes with previous instance
# https://www.javatpoint.com/save-json-file-in-python
