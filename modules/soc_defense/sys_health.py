import os
import sys
import time
import threading
import subprocess

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def educational_pause(title, explanation):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}--- [MENTOR NOTE: {title}] ---{Colors.RESET}")
    print(f"{Colors.YELLOW}{explanation}{Colors.RESET}")
    print(f"{Colors.YELLOW}-------------------------------------{Colors.RESET}\n")
    time.sleep(2)

def run_command_with_spinner(command_list, message, shell=False):
    done_event = threading.Event()
    
    def spinner_task():
        symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        idx = 0
        start_time = time.time()
        while not done_event.is_set():
            elapsed = time.time() - start_time
            sys.stdout.write(f"\r{Colors.CYAN}[{symbols[idx % len(symbols)]}] {message} - Elapsed: {elapsed:.1f}s{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1
        sys.stdout.write(f"\r{Colors.GREEN}[✓] {message} - Completed in {time.time() - start_time:.1f}s{Colors.RESET}\n")

    spinner_thread = threading.Thread(target=spinner_task)
    spinner_thread.start()

    try:
        if shell:
            result = subprocess.run(command_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            result = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        result = type('obj', (object,), {'stdout': '', 'stderr': str(e), 'returncode': 1})
        
    done_event.set()
    spinner_thread.join()
    
    return result

def check_dependencies():
    educational_pause("Phase 1: Toolchain Validation", 
                    @@"A SecOps environment is useless without its weapons. We are running 'which' commands to query the system PATH and verify our core utilities (Docker, Nmap, Wireshark) are installed.")
    
    tools = ['docker', 'nmap', 'wireshark', 'brew']
    missing = []
    
    for tool in tools:
        res = run_command_with_spinner(["which", tool], f"Checking for {tool}")
        if res.returncode != 0:
            missing.append(tool)
            
    if missing:
        print(f"\n{Colors.RED}[!] Critical tools missing: {', '.join(missing)}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Action required: Install these before conducting heavy audits.{Colors.RESET}")
    else:
        print(f"\n{Colors.GREEN}[+] All core SecOps tools verified and present.{Colors.RESET}")

def check_brew_updates():
    educational_pause("Phase 2: Third-Party Package Audit (Homebrew)", 
                    @@"Outdated local packages are the easiest vector for privilege escalation. We are querying Homebrew to see if any of our installed libraries have known vulnerabilities that require patching.")
    
    res = run_command_with_spinner(["brew", "outdated"], "Querying Homebrew for outdated packages")
    
    if res.returncode == 0:
        outdated = res.stdout.strip().split('\n')
        outdated = [pkg for pkg in outdated if pkg] 
        
        if len(outdated) > 0:
            print(f"\n{Colors.YELLOW}[!] Found {len(outdated)} outdated packages.{Colors.RESET}")
            print(f"Run 'brew upgrade' to patch them.")
        else:
            print(f"\n{Colors.GREEN}[+] All third-party packages are fully patched.{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}[!] Failed to query Homebrew. Is it installed correctly?{Colors.RESET}")

def check_macos_updates():
    educational_pause("Phase 3: Kernel & OS Patch Level", 
                    @@"Sandbox escapes and kernel panics occur when the core OS is vulnerable. We are now establishing a secure connection to Apple's update servers to fetch the latest macOS baseline. (This usually takes 15-30 seconds).")
    
    res = run_command_with_spinner(["softwareupdate", "-l"], "Querying Apple servers for macOS updates")
    
    if "No new software available" in res.stderr or "No new software available" in res.stdout:
        print(f"\n{Colors.GREEN}[+] macOS is fully updated. Host OS secured.{Colors.RESET}")
    elif res.returncode == 0:
        print(f"\n{Colors.YELLOW}[!] macOS Updates Available!{Colors.RESET}")
        print(f"{Colors.YELLOW}Run 'softwareupdate -i -a' to install all pending updates.{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}[!] Failed to query Apple servers. Check internet connection.{Colors.RESET}")

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}--- INITIATING SOC SYSTEM HEALTH AUDIT ---{Colors.RESET}\n")
    time.sleep(1)
    
    check_dependencies()
    time.sleep(1)
    
    check_brew_updates()
    time.sleep(1)
    
    check_macos_updates()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}--- AUDIT COMPLETE. RETURNING CONTROL ---{Colors.RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Audit aborted by user.{Colors.RESET}")
        sys.exit(1)
