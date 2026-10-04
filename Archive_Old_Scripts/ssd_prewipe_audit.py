#!/usr/bin/env python3
import os
from collections import defaultdict
def run_ssd_audit():
    print("\n" + "="*60)
    print("🔍 EXTERNAL SSD PRE-WIPE RECONNAISSANCE")
    print("="*60)
    volumes_dir = "/Volumes"
    skip_volumes = ["Macintosh HD", "Recovery", "Preboot", "VM", "Data", "Macintosh HD - Data"]
    ssd_volumes = []
    if os.path.exists(volumes_dir):
        for v in os.listdir(volumes_dir):
            if v not in skip_volumes and not v.startswith('.'):
                ssd_volumes.append(os.path.join(volumes_dir, v))
    if not ssd_volumes:
        print("[!] No external volumes detected.")
        return
    file_types = defaultdict(int)
    total_files = 0
    total_size_bytes = 0
    for vol in ssd_volumes:
        print(f"\n⏳ Scanning {vol} ...")
        try:
            for root, dirs, files in os.walk(vol):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.startswith('.'):
                        continue
                    total_files += 1
                    file_path = os.path.join(root, file)
                    try:
                        total_size_bytes += os.path.getsize(file_path)
                    except OSError:
                        pass
                    _, ext = os.path.splitext(file)
                    ext = ext.lower()
                    if not ext:
                        ext = 'no_extension'
                    file_types[ext] += 1
        except PermissionError:
            pass
    total_size_gb = total_size_bytes / (1024 ** 3)
    print("\n" + "="*60)
    print("📊 SSD CONTENTS REPORT")
    print("="*60)
    print(f"Total Files Found: {total_files:,}")
    print(f"Total Data Size:   {total_size_gb:.2f} GB\n")
    sorted_types = sorted(file_types.items(), key=lambda item: item[1], reverse=True)
    for ext, count in sorted_types[:20]:
        print(f"  ├── {ext.ljust(15)} : {count:,} files")
    print("\n" + "="*60)
    print("⚠️  REVIEW THIS CAREFULLY BEFORE WIPING /DEV/DISK4")
    print("="*60 + "\n")
if __name__ == "__main__":
    run_ssd_audit()
