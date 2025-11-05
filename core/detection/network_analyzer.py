import psutil
import socket
from colorama import Fore, Style

class NetworkAnalyzer:
    def __init__(self):
        self.suspicious_ports = [4444, 1337, 31337, 12345, 9999, 5555, 6666, 9999]
        self.known_backdoor_ports = [4444, 1337, 31337]  # Common backdoor ports
    
    def analyze_connections(self):
        """Check network connections for suspicious activity"""
        print(f"{Fore.CYAN}[+] Analyzing network connections...{Style.RESET_ALL}")
        
        try:
            connections = psutil.net_connections(kind='inet')
            print(f"[+] Found {len(connections)} active connections")
            
            suspicious_count = 0
            
            for conn in connections:
                if self.is_suspicious_connection(conn):
                    suspicious_count += 1
                    self.print_suspicious_connection(conn)
            
            if suspicious_count == 0:
                print(f"{Fore.GREEN}[✅] No suspicious network connections detected!{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Found {suspicious_count} suspicious connections{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}[-] Error analyzing network: {e}{Style.RESET_ALL}")
    
    def is_suspicious_connection(self, conn):
        """Check if network connection looks suspicious"""
        # Check local ports
        if hasattr(conn.laddr, 'port') and conn.laddr.port in self.suspicious_ports:
            return True
        
        # Check remote ports  
        if conn.raddr and hasattr(conn.raddr, 'port') and conn.raddr.port in self.suspicious_ports:
            return True
        
        # Check for established connections on backdoor ports
        if conn.status == 'ESTABLISHED' and conn.raddr:
            if conn.raddr.port in self.known_backdoor_ports:
                return True
        
        return False
    
    def print_suspicious_connection(self, conn):
        """Display details about suspicious connection"""
        print(f"{Fore.RED}[🚨] SUSPICIOUS CONNECTION:{Style.RESET_ALL}")
        print(f"    PID: {conn.pid}")
        
        # Get process name
        try:
            if conn.pid:
                process = psutil.Process(conn.pid)
                print(f"    Process: {process.name()}")
        except:
            print(f"    Process: Unknown")
        
        # Local address info
        if hasattr(conn.laddr, 'ip') and hasattr(conn.laddr, 'port'):
            print(f"    Local: {conn.laddr.ip}:{conn.laddr.port}")
        
        # Remote address info
        if conn.raddr and hasattr(conn.raddr, 'ip') and hasattr(conn.raddr, 'port'):
            print(f"    Remote: {conn.raddr.ip}:{conn.raddr.port}")
        
        print(f"    Status: {conn.status}")
        print()