import subprocess
import sys
import time

def run_with_telemetry(command, task_name):
print(f"\n🏥 [TRIAGE] Initiating procedure: {task_name}")
print(f"🩺 Monitoring vital signs (This may take several minutes)...\n")

start_time = time.time()

process = subprocess.Popen(
command,
shell=True,
stdout=subprocess.PIPE,
stderr=subprocess.STDOUT,
text=True,
bufsize=1
)

spinner = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣"]
spin_idx = 0

try:
for line in process.stdout:
line = line.strip()
display_line = (line[:75] + '...') if len(line) > 75 else line
sys.stdout.write(f"\r{spinner[spin_idx % len(spinner)]} [PACKING] {display_line}".ljust(100))
sys.stdout.flush()
spin_idx += 1

process.wait()

elapsed = int(time.time() - start_time)
mins, secs = divmod(elapsed, 60)

if process.returncode == 0:
print(f"\n\n✅ [DISCHARGE] Procedure complete! The data is stable.")
print(f"⏱️  Total Operation Time: {mins} minutes, {secs} seconds.\n")
else:
print(f"\n\n⚠️ [CODE YELLOW] Procedure finished, but reported an error code: {process.returncode}\n")

except KeyboardInterrupt:
print(f"\n\n🛑 [ABORT] Procedure cancelled by operator.")
process.terminate()

if name == "main":
cmd = "tar -czvf /Volumes/SecOps_Vault/Extras_and_Keys_2026.tar.gz ~/Downloads ~/Movies ~/Music ~/.ssh ~/.zshrc ~/.aws ~/Library/Application\ Support/MobileSync/Backup 2>/dev/null"
run_with_telemetry(cmd, "Cold Storage: Extras & Keys")
