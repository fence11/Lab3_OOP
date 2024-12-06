import os
import hashlib
import json
from datetime import datetime


class FileSnapshot:
    def __init__(self, path, hash_value=None, last_modified=None):
        self.path = path
        self.hash = hash_value or self.compute_hash()
        self.last_modified = last_modified or os.path.getmtime(path)

    def compute_hash(self):
        try:
            with open(self.path, "rb") as file:
                file_content = file.read()
                return hashlib.sha256(file_content).hexdigest()
        except (IOError, FileNotFoundError) as e:
            print(f"Error reading file: {e}")
            return None

    def compare(self, other):
        if self.hash != other.hash:
            return "Change detected"
        return "No change"

    def to_dict(self):
        return {
            "path": self.path,
            "hash": self.hash,
            "last_modified": self.last_modified,
        }

    @staticmethod
    def from_dict(data):
        return FileSnapshot(data["path"], data["hash"], data["last_modified"])


class FolderMonitor:
    SNAPSHOT_FILE = "folder_snapshot.json"

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.snapshots = {}
        self.load_snapshots()

    def load_snapshots(self):
        if os.path.exists(self.SNAPSHOT_FILE):
            with open(self.SNAPSHOT_FILE, "r") as file:
                data = json.load(file)
                self.snapshots = {
                    path: FileSnapshot.from_dict(snap) for path, snap in data.items()
                }

    def save_snapshots(self):
        with open(self.SNAPSHOT_FILE, "w") as file:
            json.dump(
                {path: snap.to_dict() for path, snap in self.snapshots.items()},
                file,
                indent=4,
            )

    def take_snapshot(self):
        snapshots = {}
        for file_name in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file_name)
            if os.path.isfile(file_path):
                snapshots[file_name] = FileSnapshot(file_path)
        self.snapshots = snapshots

    def detect_changes(self):
        current_snapshots = {}
        changes = {}

        for file_name in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file_name)
            if os.path.isfile(file_path):
                current_snapshots[file_name] = FileSnapshot(file_path)

        for file_name, snapshot in current_snapshots.items():
            if file_name not in self.snapshots:
                changes[file_name] = "New file"
            else:
                changes[file_name] = snapshot.compare(self.snapshots[file_name])

        for file_name in self.snapshots:
            if file_name not in current_snapshots:
                changes[file_name] = "File deleted"

        return changes

    def display_changes(self, changes):
        snapshot_time = datetime.now().strftime("%d/%m/%Y; %H:%M:%S.%f")[:-3]
        print(f"Last snapshot created at: {snapshot_time}")
        for file_name, status in changes.items():
            print(f"{file_name} - {status}")


if __name__ == "__main__":
    folder_path = "testing_files"

    print(f"Current working directory: {os.getcwd()}")
    print(f"Checking folder: {folder_path}")

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        exit(1)

    monitor = FolderMonitor(folder_path)

    print("Checking folder for changes...")
    changes = monitor.detect_changes()
    monitor.display_changes(changes)

    print("\nUpdating snapshot...")
    monitor.take_snapshot()
    monitor.save_snapshots()
    print("Snapshot updated.")
