import time
import sys
import os

# Terminal Colors
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Telemetry Spinner
def spinner(duration, message):
    symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start_time = time.time()
    idx = 0
    while (time.time() - start_time) < duration:
        elapsed = time.time() - start_time
        sys.stdout.write(f"\r{Colors.CYAN}[{symbols[idx % len(symbols)]}] {message} - Elapsed: {elapsed:.1f}s{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    sys.stdout.write(f"\r{Colors.GREEN}[✓] {message} - Completed in {duration:.1f}s{Colors.RESET}\n")

# Educational Echo
def educational_pause(title, explanation):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}--- [MENTOR NOTE: {title}] ---{Colors.RESET}")
    print(f"{Colors.YELLOW}{explanation}{Colors.RESET}")
    print(f"{Colors.YELLOW}-------------------------------------{Colors.RESET}\n")
    time.sleep(2)

def main():
    print(f"{Colors.BOLD}{Colors.CYAN}Initializing Forensic MRI Sequence...{Colors.RESET}\n")
    time.sleep(1)

    educational_pause("Patient Intake (Initialization)", "Verifying tool availability, checking permissions, and ensuring our output directories are secure and isolated. We don't want cross-contamination.")
    spinner(3, "Patient Intake: Verifying tool paths and permissions")

    educational_pause("Contrast Injection (Pre-Scan Config)", "A SYN scan sends a SYN packet, waits for a SYN-ACK, and tears down the connection with a RST. We are configuring our tools to look for specific 'anomalies'.")
    spinner(4, "Administering Contrast: Configuring SYN scan parameters")

    educational_pause("The MRI Scan (Execution)", "The scanner is actively probing the target. We are looking for 'lesions' or 'abnormalities' representing potential vulnerabilities.")
    spinner(6, "Scanning: Acquiring high-resolution target images")

    educational_pause("Vitals Review (Analysis)", "The scan is complete. Now we parse the raw output. We separate the noise from the signal, identifying true anomalies. This is the triage phase.")
    spinner(3, "Vitals Review: Parsing scan telemetry and identifying anomalies")

    educational_pause("Quarantine (Reporting/Output)", "Any identified 'abnormalities' are isolated for further study. We generate a report detailing the 'patient's' condition based on our scan.")
    spinner(2, "Quarantine: Generating final diagnostic report")

    print(f"\n{Colors.BOLD}{Colors.GREEN}Forensic MRI Sequence Complete. See diagnostic report for details.{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Sequence aborted by user.{Colors.RESET}")
        sys.exit(1)
