#!/usr/bin/env python3
import os
from collections import defaultdict

def run_triage():
    print("\n" + "="*60)
    print("🔎 MAC & iCLOUD DATA RECONNAISSANCE")
    print("="*60)

    home = os.path.expanduser("~")
    target_locations = [
        ("Desktop", os.path.join(home, "Desktop")),
        ("Documents", os.path.join(home, "Documents")),
        ("Downloads", os.path.join(home, "Downloads")),
        ("iCloud Drive", os.path.join(home, "Library", "Mobile Documents", "com~apple~CloudDocs"))
    ]

    file_types = defaultdict(int)
    total_files = 0
    total_size_bytes = 0

    print("\n⏳ Scanning core directories recursively... (This might take a minute)")
    
    for name, target_dir in target_locations:
        if not os.path.exists(target_dir):
            print(f"  [!] Skipping {name} (Not found)")
            continue
            
        print(f"  -> Scanning {name}...")
        
        for root, dirs, files in os.walk(target_dir):
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

    total_size_gb = total_size_bytes / (1024 ** 3)

    print("\n" + "="*60)
    print("📊 TRIAGE REPORT")
    print("="*60)
    print(f"Total Files Found: {total_files:,}")
    print(f"Total Data Size:   {total_size_gb:.2f} GB\n")

    print("📑 FILE BREAKDOWN BY EXTENSION:")
    
    sorted_types = sorted(file_types.items(), key=lambda item: item[1], reverse=True)
    
    # Only print the top 30 file types so it doesn't flood your screen
    for ext, count in sorted_types[:30]:
        print(f"  ├── {ext.ljust(15)} : {count:,} files")

    print("\n" + "="*60)
    print("🟢 NEXT STEPS:")
    print("Once we know what file types you have, we can write a script to automatically")
    print("route them into folders like /Documents, /Photos, /Code, and /Archives.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_triage()
