"""
Setup Local MongoDB Portable Instance for EduPath.

Downloads MongoDB Community Server binaries, extracts mongod.exe to backend/mongodb/bin/,
creates the data directory at backend/data/db, and starts mongod locally on port 27017.
"""

import os
import sys
import zipfile
import subprocess
import urllib.request
from pathlib import Path
from pymongo import MongoClient

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = WORKSPACE_ROOT / "backend"
MONGODB_DIR = BACKEND_DIR / "mongodb"
DATA_DB_DIR = BACKEND_DIR / "data" / "db"
ZIP_PATH = BACKEND_DIR / "mongodb_dist.zip"

MONGODB_ZIP_URL = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.14.zip"

def download_mongodb():
    if (MONGODB_DIR / "bin" / "mongod.exe").exists():
        print("--> mongod.exe already present.")
        return

    print(f"--> Downloading portable MongoDB zip from {MONGODB_ZIP_URL}...")
    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(100.0, downloaded / total_size * 100) if total_size > 0 else 0
        sys.stdout.write(f"\r    Progress: {percent:.1f}% ({downloaded // (1024*1024)} MB / {total_size // (1024*1024)} MB)")
        sys.stdout.flush()

    urllib.request.urlretrieve(MONGODB_ZIP_URL, ZIP_PATH, show_progress)
    print("\n--> Download complete. Extracting mongod.exe...")

    MONGODB_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith("mongod.exe") or file.endswith(".dll"):
                filename = os.path.basename(file)
                if filename:
                    target = MONGODB_DIR / "bin" / filename
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with zip_ref.open(file) as source, open(target, "wb") as target_file:
                        target_file.write(source.read())

    print(f"--> Extracted binaries to {MONGODB_DIR / 'bin'}")
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

def start_mongod():
    DATA_DB_DIR.mkdir(parents=True, exist_ok=True)
    mongod_exe = MONGODB_DIR / "bin" / "mongod.exe"

    if not mongod_exe.exists():
        print(f"ERROR: mongod.exe not found at {mongod_exe}")
        sys.exit(1)

    print(f"--> Starting local mongod process on port 27017 with dbpath: {DATA_DB_DIR}...")
    cmd = [
        str(mongod_exe),
        "--dbpath", str(DATA_DB_DIR),
        "--port", "27017",
        "--logpath", str(BACKEND_DIR / "data" / "mongod.log"),
        "--logappend"
    ]

    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    print("--> Process launched. Verifying connection...")

def verify_connection():
    import time
    for attempt in range(1, 10):
        try:
            client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
            client.admin.command('ping')
            print("--> SUCCESS: Connected to local MongoDB instance on port 27017!")
            print(f"--> Database 'edupath' is ready for use.")
            return True
        except Exception:
            time.sleep(1)
            print(f"    Waiting for mongod to initialize (attempt {attempt}/10)...")
    print("--> FAILED to ping local MongoDB.")
    return False

if __name__ == "__main__":
    download_mongodb()
    start_mongod()
    success = verify_connection()
    if not success:
        sys.exit(1)
