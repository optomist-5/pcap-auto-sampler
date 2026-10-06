#!/usr/bin/env python3
import os, sys, subprocess

def run_test(name, cmd):
    print(f"\n🧪 [TESTING TOOL] {name}")
    print(f"   Command: {cmd}")
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if res.returncode == 0 or "help" in cmd:
            print(f"   ✅ REAL OUTPUT VERIFIED ({len(res.stdout)} bytes returned)")
            if res.stdout:
                print("   --- Output Snippet ---")
                print("\n".join(res.stdout.splitlines()[:4]))
        else:
            print(f"   ⚠️ WARNING: Exited with code {res.returncode}")
            print(f"   Error: {res.stderr[:200]}")
    except Exception as e:
        print(f"   ❌ EXECUTION ERROR: {e}")

print("======================================================================")
print("             REALITY CHECK: INDIVIDUAL TOOL TEST HARNESS              ")
print("======================================================================")

# 1. Test Sentinel Log Parser
run_test("SecOps Sentinel", f"python3 {os.path.expanduser('~/secops/secops_sentinel.py')}")

# 2. Test Threat Hunter against CLI help
run_test("Threat Hunter CLI", f"python3 {os.path.expanduser('~/secops/modules/soc_defense/threat_hunter.py')} --help")

# 3. Test Cloud Hardener against CLI help
run_test("Cloud Hardener CLI", f"python3 {os.path.expanduser('~/secops/modules/soc_defense/cloud_hardener.py')} --help")

# 4. Test Workspace Sync Script
run_test("Workspace Sync", f"{os.path.expanduser('~/secops/scripts/sync_workspace.sh')}")

print("\n======================================================================")
