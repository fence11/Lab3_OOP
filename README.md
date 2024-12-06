# Lab3_OOP

Src:
https://stackoverflow.com/questions/30226891/how-to-compare-two-versions-of-same-file-old-and-new-and-detect-if-there-were
 - maybe use hash to check fiel changes instead of reading file instances ?
https://www.geeksforgeeks.org/how-to-detect-file-changes-using-python/
 - use this for reference

## Features

- **File Hashing**: Computes the SHA-256 hash of each file to track content changes.
- **Snapshot Management**: Saves and loads folder snapshots in a JSON file for monitoring.
- **Change Detection**:
  - Detects new files.
  - Identifies modified files by comparing their hashes.
  - Flags deleted files.
  - Displays detected changes with timestamps.

## **FileSnapshot Class**

Represents a snapshot of a file at a specific point in time.

### **Methods**

1. **`__init__(self, path, hash_value=None, last_modified=None)`**
   - Initializes a `FileSnapshot` object.
   - **Parameters:**
     - `path`: Path to the file.
     - `hash_value`: (Optional) Precomputed hash value of the file.
     - `last_modified`: (Optional) Last modified timestamp of the file.
   - If `hash_value` or `last_modified` is not provided, computes these values automatically.

2. **`_compute_hash(self)`**
   - Calculates the SHA-256 hash of the file contents.
   - **Returns:** The hash as a hexadecimal string.
   - Handles errors like missing or inaccessible files gracefully.

3. **`compare(self, other)`**
   - Compares the current snapshot with another `FileSnapshot`.
   - **Parameters:**
     - `other`: Another `FileSnapshot` to compare with.
   - **Returns:**
     - `"Change detected"` if the hashes differ.
     - `"No change"` if the hashes are the same.

4. **`to_dict(self)`**
   - Converts the `FileSnapshot` object into a dictionary for easy storage.
   - **Keys:** `path`, `hash`, `last_modified`.

5. **`from_dict(data)` (Static Method)**
   - Creates a `FileSnapshot` object from a dictionary.
   - **Parameters:**
     - `data`: Dictionary with keys `path`, `hash`, and `last_modified`.

---

## **FolderMonitor Class**

Monitors a folder for changes and maintains a snapshot of its state.

### **Methods**

1. **`__init__(self, folder_path)`**
   - Initializes the `FolderMonitor`.
   - **Parameters:**
     - `folder_path`: Path to the folder to monitor.
   - Automatically loads existing snapshots from `folder_snapshot.json` if available.

2. **`load_snapshots(self)`**
   - Loads snapshots from the `folder_snapshot.json` file.
   - Populates the `self.snapshots` dictionary, mapping file paths to `FileSnapshot` objects.

3. **`save_snapshots(self)`**
   - Saves the current snapshots to the `folder_snapshot.json` file in JSON format.

4. **`take_snapshot(self)`**
   - Captures the current state of all files in the monitored folder.
   - Updates `self.snapshots` with new snapshots of all files.

5. **`detect_changes(self)`**
   - Compares the current state of the folder with the last saved snapshot.
   - **Returns:** A dictionary of detected changes:
     - New files: `"New file"`
     - Modified files: `"Change detected"`
     - Deleted files: `"File deleted"`

6. **`display_changes(self, changes)`**
   - Displays detected changes in a user-friendly format.
   - **Parameters:**
     - `changes`: Dictionary of file changes (output of `detect_changes`).
