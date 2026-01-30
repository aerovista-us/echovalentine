import os
import json
import csv
import argparse
from datetime import datetime
import platform
import socket
import getpass
import hashlib
import concurrent.futures

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

EXCLUDED_DIRS = {'node_modules', '.git', '__pycache__', 'venv', 'env', '$recycle.bin', 'system volume information'}
UI_FILES = {'index.html', 'style.css', 'tailwind.config.js'}
LOGIC_FILES = {'main.js', 'preload.js', 'app.js'}
CONFIG_FILES = {'package.json', 'vite.config.js', 'webpack.config.js'}
ASSET_EXTS = {'.png', '.jpg', '.svg', '.md', '.txt', '.env'}

def detect_party(full_path):
    path = full_path.lower()
    ext = os.path.splitext(full_path)[1].lower()
    if ext == ".mp3":
        return "EchoVerse Audio"
    elif ext == ".mp4":
        return "AeroVista - Lumina"
    elif ext in [".ppt", ".pptx"]:
        return "Inspiro/Boost/Dish"
    if "aerovista" in path:
        return "AeroVista"
    elif "skyforge" in path:
        return "AeroVista - SkyForge"
    elif "summit" in path:
        return "AeroVista - Summit"
    elif "vespera" in path:
        return "AeroVista - Vespera"
    elif "lumina" in path:
        return "AeroVista - Lumina"
    elif "horizon" in path:
        return "AeroVista - Horizon Aerial"
    elif "nexus" in path:
        return "AeroVista - Nexus TechWorks"
    elif "inpsiro" in path or "boost" in path or "dish" in path:
        return "Inspiro/Boost/Dish"
    elif "personal" in path or "timbr" in path or "trcam" in path:
        return "Personal"
    else:
        return "Unknown"

def file_hash(path, block_size=65536):
    """Calculates the MD5 hash of a file for speed."""
    try:
        hasher = hashlib.md5()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                hasher.update(block)
        return hasher.hexdigest()
    except Exception as e:
        return f"ERROR:{e}"

def parse_package_json(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            pkg = json.load(f)
        return {
            "app_name": pkg.get("name", ""),
            "description": pkg.get("description", ""),
            "dependencies": list(pkg.get("dependencies", {}).keys()),
            "has_electron": "electron" in pkg.get("dependencies", {}),
            "has_tailwind": "tailwindcss" in pkg.get("dependencies", {}),
            "scripts": list(pkg.get("scripts", {}).keys()),
            "pkg_main": pkg.get("main", ""),
            "pkg_version": pkg.get("version", "")
        }
    except Exception as e:
        return {
            "app_name": "",
            "description": f"Failed to parse package.json: {e}",
            "dependencies": [],
            "has_electron": False,
            "has_tailwind": False,
            "scripts": [],
            "pkg_main": "",
            "pkg_version": ""
        }

def classify_file(file, parent_dir):
    fname = file.lower()
    ext = os.path.splitext(file)[1].lower()
    if fname in UI_FILES or ext in {'.css', '.html'}:
        return "ui_core"
    elif fname in LOGIC_FILES or ext in {'.js', '.ts'}:
        return "logic_core"
    elif fname in CONFIG_FILES:
        return "config"
    elif ext in ASSET_EXTS:
        return "content_asset"
    elif parent_dir == "node_modules":
        return "dependency"
    return "general"

def process_file(args):
    root, file, path, root_metadata = args
    full_path = os.path.join(root, file)
    try:
        stat = os.stat(full_path)
        metadata = {
            "file_name": file,
            "full_path": full_path,
            "size_bytes": stat.st_size,
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "last_accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "extension": os.path.splitext(file)[1].lower(),
            "subrole": classify_file(file, os.path.basename(root)),
            "host": socket.gethostname(),
            "username": getpass.getuser(),
            "os": platform.system(),
            "os_version": platform.version(),
            "scan_timestamp": datetime.now().isoformat(),
            "parent_folder": os.path.basename(root),
            "root_folder": os.path.basename(path),
            "responsible_party": detect_party(full_path),
            "file_hash": file_hash(full_path)
        }
        # Merge the app container metadata
        metadata.update(root_metadata)
        return metadata
    except Exception as e:
        return {
            "file_name": file,
            "full_path": full_path,
            "error": str(e)
        }

def scan_directory(path, quiet=False):
    tasks = []
    for root, dirs, files in os.walk(path):
        # More robust exclusion
        root_lower = root.lower()
        if any(excl in root_lower for excl in EXCLUDED_DIRS):
            dirs[:] = [] # Don't recurse into excluded directories
            continue

        root_metadata = {}
        is_app_container = 'package.json' in files and ('index.html' in files or 'main.js' in files)
        root_metadata["is_app_container"] = is_app_container
        if is_app_container:
            pkg_path = os.path.join(root, 'package.json')
            pkg_data = parse_package_json(pkg_path)
            root_metadata.update(pkg_data)

        for file in files:
            tasks.append((root, file, path, root_metadata))

    inventory = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if not quiet and tqdm:
            results = tqdm(executor.map(process_file, tasks), total=len(tasks), desc="Processing files", unit="file")
        else:
            results = executor.map(process_file, tasks)
        
        inventory = [r for r in results if r]

    # Deduplication
    hash_map = {}
    for entry in inventory:
        h = entry.get("file_hash", "")
        if h.startswith("ERROR") or h == "":
            entry["is_duplicate"] = False
            entry["duplicate_of"] = ""
            continue
        if h in hash_map:
            entry["is_duplicate"] = True
            entry["duplicate_of"] = hash_map[h]
        else:
            entry["is_duplicate"] = False
            entry["duplicate_of"] = ""
            hash_map[h] = entry["full_path"]

    return inventory

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="📁 Enhanced Full-Feature App Scanner")
    parser.add_argument("--path", default=".", help="Directory path to scan")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")
    args = parser.parse_args()

    inventory = scan_directory(args.path, quiet=args.quiet)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Handle case where path is '.'
    abs_path = os.path.abspath(args.path)
    folder_name = os.path.basename(abs_path)
    out_file = f"{folder_name}_inventory_{timestamp}.csv"

    if inventory:
        # Dynamically get all keys from all records
        all_keys = set()
        for item in inventory:
            all_keys.update(item.keys())
        
        # Sort keys for consistent column order
        # Put important keys first
        key_order = ['full_path', 'file_name', 'size_bytes', 'last_modified', 'is_duplicate', 'duplicate_of', 'app_name', 'description']
        sorted_keys = key_order + sorted([k for k in all_keys if k not in key_order])

        with open(out_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=sorted_keys)
            writer.writeheader()
            writer.writerows(inventory)
        print(f"[✓] Inventory saved to: {out_file}")
    else:
        print("[X] No inventory data found.")