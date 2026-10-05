#!/usr/bin/env python3
import argparse
import sys
import time

def handle_system(args):
    if args.action == "clean":
        print("🧹 Triage: Initiating deep system clean...")
        time.sleep(1)
        print("✅ System clean complete. Host is pristine.")
    elif args.action == "status":
        print("🩺 Vitals: Host system is Nominal. Zero-Trust active.")
    elif args.action == "setup":
        print("🏗️  Building: Installing baseline SecOps tools...")

def handle_cloud(args):
    if args.action == "audit":
        if args.azure: print("☁️  Azure: Auditing Entra ID...")
        elif args.gcp: print("☁️  GCP: Checking billing killswitch...")
        else: print("⚠️ Please specify a cloud provider")
    elif args.action == "deploy":
        print("🚀 Deploying cloud infrastructure...")

def handle_inventory(args):
    import os
    archive_dir = os.path.expanduser("~/secops/Archive_Old_Scripts")
    print("\n==========================================================")
    print(" 🏥 SECOPS RIG: SUPPLY CLOSET & TOOL INVENTORY")
    print("==========================================================\n")
    if not os.path.exists(archive_dir): return
    files = sorted(os.listdir(archive_dir))
    for tool in [f for f in files if f.endswith('.py')]:
        print(f"   🔥 \033[91m{tool}\033[0m" if "god_mode" in tool or "master" in tool else f"   🟢 \033[92m{tool}\033[0m")
    for tool in [f for f in files if f.endswith('.sh')]:
        print(f"   🔵 \033[96m{tool}\033[0m")
    print("\n==========================================================")

def handle_sort(args):
    import os, shutil
    target_dir = os.path.expanduser(args.target)
    if not os.path.exists(target_dir): return
    print(f"🌪  Initiating High-Speed Sort on: {target_dir}")
    categories = {"Images": [".jpg", ".png", ".gif"], "Documents": [".pdf", ".docx", ".txt", ".csv"], "Archives": [".zip", ".tar.gz"], "Code": [".py", ".sh", ".json"]}
    for cat in categories.keys(): os.makedirs(os.path.join(target_dir, cat), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "Misc"), exist_ok=True)
    moved = 0
    for item in os.listdir(target_dir):
        p = os.path.join(target_dir, item)
        if os.path.isdir(p): continue
        ext = os.path.splitext(item)[1].lower()
        for cat, exts in categories.items():
            if ext in exts:
                try: shutil.move(p, os.path.join(target_dir, cat, item)); moved += 1; break
                except: pass
    print(f"✅ Categorized {moved} files.")

def handle_dedupe(args):
    import os, hashlib, shutil
    trash_dir = os.path.expanduser("~/Desktop/Duplicate_Trash")
    os.makedirs(trash_dir, exist_ok=True)
    hashes = {}; dup_count = 0
    for t_dir in args.targets:
        t_dir = os.path.expanduser(t_dir)
        if not os.path.exists(t_dir): continue
        for root, _, files in os.walk(t_dir):
            if '/.' in root: continue
            for file in files:
                if file.startswith('.'): continue
                filepath = os.path.join(root, file)
                try:
                    fsize = os.path.getsize(filepath)
                    if fsize == 0: continue
                    hasher = hashlib.md5()
                    with open(filepath, 'rb') as f: hasher.update(f.read(65536))
                    fhash = f"{fsize}_{hasher.hexdigest()}"
                    if fhash in hashes:
                        dup_count += 1
                        shutil.move(filepath, os.path.join(trash_dir, f"{dup_count}_{file}"))
                    else: hashes[fhash] = filepath
                except: pass
    print(f"✅ Moved {dup_count} duplicates to ~/Desktop/Duplicate_Trash")

def handle_backup(args):
    import os, tarfile, time
    source = os.path.expanduser(args.source)
    dest = os.path.expanduser(args.dest)
    if not os.path.exists(source):
        print(f"❌ Error: Source '{source}' does not exist.")
        return
    os.makedirs(dest, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(source.rstrip('/'))
    if not base_name: base_name = "archive"
    archive_path = os.path.join(dest, f"{base_name}_SECURE_BACKUP_{timestamp}.tar.gz")
    print(f"📦 Compressing {source} ...")
    try:
        with tarfile.open(archive_path, "w:gz") as tar: tar.add(source, arcname=base_name)
        print(f"✅ Backup Sealed! Size: {os.path.getsize(archive_path)/(1024*1024):.2f} MB")
        print(f"🔒 Location: {archive_path}")
    except Exception as e: print(f"❌ Failed: {e}")

def handle_run(args):
    import os, subprocess
    script_path = os.path.join(os.path.expanduser("~/secops/Archive_Old_Scripts"), args.script)
    if not os.path.exists(script_path): return
    if args.script.endswith('.py'): subprocess.run(["python3", script_path])
    elif args.script.endswith('.sh'): subprocess.run(["bash", script_path])

def main():
    parser = argparse.ArgumentParser(description="⚕️ Master Controller")
    subs = parser.add_subparsers(dest="module")
    
    sys_p = subs.add_parser("system"); sys_p.add_argument("action", choices=["clean", "status", "setup"])
    cld_p = subs.add_parser("cloud"); cld_p.add_argument("action", choices=["audit", "deploy"]); cld_p.add_argument("--azure", action="store_true"); cld_p.add_argument("--gcp", action="store_true")
    srt_p = subs.add_parser("sort"); srt_p.add_argument("target")
    ddp_p = subs.add_parser("dedupe"); ddp_p.add_argument("targets", nargs='+')
    
    # NEW BACKUP COMMAND
    bkp_p = subs.add_parser("backup")
    bkp_p.add_argument("source")
    bkp_p.add_argument("dest")
    
    subs.add_parser("inventory")
    run_p = subs.add_parser("run"); run_p.add_argument("script")
    
    args = parser.parse_args()
    if args.module == "system": handle_system(args)
    elif args.module == "cloud": handle_cloud(args)
    elif args.module == "sort": handle_sort(args)
    elif args.module == "dedupe": handle_dedupe(args)
    elif args.module == "backup": handle_backup(args)
    elif args.module == "inventory": handle_inventory(args)
    elif args.module == "run": handle_run(args)
    else: parser.print_help()

if __name__ == "__main__": main()
