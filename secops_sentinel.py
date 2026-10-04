#!/usr/bin/env python3
"""
SecOps Sentinel - Interactive Terminal Suite & Vault Sanitizer
"""
import sys
import os
import shutil
import subprocess
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.panel import Panel

console = Console()

EXCLUDE_PATTERNS = [
    "citrix", "ica", "receiver", "workspace", "vpn", "session",
    "cookies", "cache", "cacheddata", "code cache", "gpu-cache",
    "local storage", "session storage", "indexeddb", "webstorage",
    ".ds_store", "thumbs.db", "saved state", "logs", "log",
    "crashreporter", "diagnosticreports", "tmp", "temp", "caches"
]

def render_banner():
    banner_text = "[bold cyan]SecOps Sentinel[/bold cyan] | [bold green]Active Environment[/bold green]\n[dim]High-Observability Interactive Workstation CLI[/dim]"
    console.print(Panel(banner_text, border_style="cyan"))

def is_junk(path):
    path_lower = path.lower()
    return any(pattern in path_lower for pattern in EXCLUDE_PATTERNS)

def scrub_existing_vault(vault_dir):
    dst = os.path.expanduser(vault_dir)
    if not os.path.exists(dst):
        console.print(f"[bold red]Error:[/bold red] Vault path '{dst}' does not exist.")
        return

    console.print(f"\n[bold yellow]Scanning '{dst}' for junk artifacts to purge...[/bold yellow]")
    junk_files = []
    
    for root, _, files in os.walk(dst):
        for f in files:
            full_path = os.path.join(root, f)
            if is_junk(full_path):
                junk_files.append(full_path)

    if not junk_files:
        console.print("[bold green]Vault is completely clean! No junk found.[/bold green]")
    else:
        console.print(f"[bold red]Found {len(junk_files)} junk files to purge.[/bold red]\n")
        for filepath in junk_files:
            try:
                os.remove(filepath)
            except Exception:
                pass

    # Safely clean up empty directories
    for root, dirs, _ in os.walk(dst, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                if os.path.exists(dir_path) and not os.listdir(dir_path):
                    os.rmdir(dir_path)
            except Exception:
                pass

    console.print("\n[bold green]✔ Vault Scrub Complete![/bold green]\n")

def check_system():
    console.print("\n[bold cyan]=== System Metrics Baseline ===[/bold cyan]\n")
    table = Table(title="Host Status Overview", border_style="bright_blue")
    table.add_column("Metric", style="bold yellow")
    table.add_column("Live Readout", style="white")

    uptime_res = subprocess.run(["uptime"], capture_output=True, text=True).stdout.strip()
    table.add_row("Uptime & Load", uptime_res)

    df_res = subprocess.run(["df", "-h", "/"], capture_output=True, text=True).stdout.splitlines()
    if len(df_res) > 1:
        table.add_row("Root Filesystem Space", df_res[1])

    console.print(table)

def check_network():
    console.print("\n[bold cyan]=== Active TCP Sockets ===[/bold cyan]\n")
    net_res = subprocess.run("netstat -an -f inet | grep TCP", shell=True, capture_output=True, text=True).stdout.splitlines()

    table = Table(title="TCP Network Connections", border_style="green")
    table.add_column("Protocol", style="cyan")
    table.add_column("Recv-Q", style="dim")
    table.add_column("Send-Q", style="dim")
    table.add_column("Local Address", style="bold white")
    table.add_column("Foreign Address", style="bold yellow")
    table.add_column("State", style="bold green")

    for line in net_res[:25]:
        parts = line.split()
        if len(parts) >= 6:
            state_color = "green" if parts[5] == "ESTABLISHED" else "dim"
            table.add_row(parts[0], parts[1], parts[2], parts[3], parts[4], f"[{state_color}]{parts[5]}[/{state_color}]")

    console.print(table)

def main():
    render_banner()
    if len(sys.argv) < 2:
        console.print("[bold red]Usage:[/bold red] python3 secops_sentinel.py [sys | net | scrub <vault_path>]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd in ["sys", "system"]:
        check_system()
    elif cmd in ["net", "nett"]:
        check_network()
    elif cmd == "scrub":
        target = sys.argv[2] if len(sys.argv) > 2 else "~/Vault_Mauri"
        scrub_existing_vault(target)

if __name__ == "__main__":
    main()
