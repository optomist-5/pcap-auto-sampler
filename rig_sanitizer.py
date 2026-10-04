import os, shutil, glob
base_dir = os.path.expanduser("~/secops")
archive_dir = os.path.join(base_dir, "Archive_Old_Scripts")
folders = ["bin", "modules/cloud", "modules/host", "modules/network", "modules/git", "logs"]
for f in folders: os.makedirs(os.path.join(base_dir, f), exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)
scripts = glob.glob(os.path.join(base_dir, "*.sh")) + glob.glob(os.path.join(base_dir, "*.py")) + glob.glob(os.path.join(base_dir, "scripts", "*"))
moved = 0
for s in scripts:
    if os.path.basename(s) not in ["rig_sanitizer.py", "secops_rig_audit.sh"]:
        try: shutil.move(s, os.path.join(archive_dir, os.path.basename(s))); moved += 1
        except: pass
print(f"✅ Desk Cleaned! Archived {moved} old scripts.")
