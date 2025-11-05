import psutil
import os
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init()

class ProcessMonitor:
    def __init__(self):
        self.suspicious_keywords = [
            'mimikatz', 'bloodhound', 'crackmapexec', 'metasploit',
            'beacon', 'payload', 'shellcode', 'revshell', 'pwncat'
        ]
        
        self.suspicious_process_names = [
            'nc.exe', 'nc', 'ncat', 'socat', 'wireshark', 'nessus',
            'nikto', 'sqlmap', 'hydra', 'john', 'hashcat'
        ]
    
    def scan_suspicious_processes(self):
        """Scan running processes for suspicious activity"""
        print(f"{Fore.CYAN}[+] Scanning {len(list(psutil.process_iter()))} running processes...{Style.RESET_ALL}")
        
        suspicious_count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
            try:
                process_info = proc.info
                
                if self.is_suspicious(process_info):
                    suspicious_count += 1
                    self.print_suspicious(process_info)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if suspicious_count == 0:
            print(f"{Fore.GREEN}[✅] No suspicious processes detected!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Found {suspicious_count} potentially suspicious processes{Style.RESET_ALL}")
    
    def is_suspicious(self, process_info):
        """Check if process shows signs of being malicious"""
        name = (process_info['name'] or '').lower()
        cmdline = ' '.join(process_info['cmdline'] or []).lower()
        
        # Check name against suspicious list
        for suspicious_name in self.suspicious_process_names:
            if suspicious_name in name:
                return True
        
        # Check command line for suspicious keywords
        for keyword in self.suspicious_keywords:
            if keyword in cmdline:
                return True
        
        # Check for hidden or unusual process characteristics
        if self.has_suspicious_characteristics(process_info):
            return True
            
        return False
    
    def has_suspicious_characteristics(self, process_info):
        """Look for unusual process characteristics"""
        name = process_info['name'] or ''
        cmdline = ' '.join(process_info['cmdline'] or [])
        
        # Empty command line can be suspicious
        if not cmdline.strip() and name:
            return True
            
        # Process with no parent (orphan) can be suspicious
        try:
            proc = psutil.Process(process_info['pid'])
            if proc.ppid() == 1 and name not in ['systemd', 'init']:
                return True
        except:
            pass
            
        return False
    
    def print_suspicious(self, process_info):
        """Display details about suspicious process"""
        print(f"{Fore.RED}[🚨] SUSPICIOUS PROCESS DETECTED:{Style.RESET_ALL}")
        print(f"    PID: {process_info['pid']}")
        print(f"    Name: {process_info['name']}")
        print(f"    User: {process_info['username']}")
        
        cmdline = process_info['cmdline'] or []
        if cmdline:
            print(f"    Command: {' '.join(cmdline[:3])}{'...' if len(cmdline) > 3 else ''}")
        
        # Get additional process info
        try:
            proc = psutil.Process(process_info['pid'])
            create_time = proc.create_time()
            memory_mb = proc.memory_info().rss / 1024 / 1024
            
            print(f"    Memory: {memory_mb:.1f} MB")
            print(f"    CPU: {proc.cpu_percent():.1f}%")
        except:
            pass
            
        print()