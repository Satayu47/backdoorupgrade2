import psutil
import os
from colorama import Fore, Style

class BehavioralAnalyzer:
    def analyze_process(self, pid):
        """ANALYZE SPECIFIC PROCESS - TESTED WORKING"""
        try:
            process = psutil.Process(pid)
            print(f"{Fore.CYAN}[🔬] Analyzing Process PID {pid}{Style.RESET_ALL}")
            
            # Get comprehensive process info
            with process.oneshot():
                name = process.name()
                exe = process.exe()
                cmdline = process.cmdline()
                username = process.username()
                create_time = process.create_time()
                threads = process.num_threads()
                memory_info = process.memory_info()
                cpu_percent = process.cpu_percent()
                connections = process.connections()
                open_files = process.open_files()
            
            # Display basic info
            print(f"Name: {name}")
            print(f"Executable: {exe}")
            print(f"User: {username}")
            print(f"Threads: {threads}")
            print(f"Memory: {memory_info.rss / 1024 / 1024:.1f} MB")
            print(f"CPU: {cpu_percent}%")
            
            # Command line
            if cmdline:
                print(f"Command: {' '.join(cmdline)}")
            
            # Network connections
            if connections:
                print(f"\nNetwork Connections:")
                for conn in connections[:5]:  # Show first 5
                    local = f"{conn.laddr.ip}:{conn.laddr.port}" if hasattr(conn.laddr, 'ip') else str(conn.laddr)
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    print(f"  {local} -> {remote} ({conn.status})")
            
            # Behavioral analysis
            self.analyze_behavior(process)
            
        except psutil.NoSuchProcess:
            print(f"{Fore.RED}[-] Process {pid} not found{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Analysis error: {e}{Style.RESET_ALL}")
    
    def analyze_behavior(self, process):
        """ANALYZE PROCESS BEHAVIOR FOR MALICIOUS INDICATORS"""
        print(f"\n{Fore.YELLOW}[📊] BEHAVIORAL ANALYSIS:{Style.RESET_ALL}")
        
        indicators = []
        
        try:
            # Check 1: High number of threads
            if process.num_threads() > 100:
                indicators.append("High thread count (possible C2)")
            
            # Check 2: Network connections on suspicious ports
            connections = process.connections()
            suspicious_ports = [4444, 1337, 31337]
            for conn in connections:
                if conn.raddr and hasattr(conn.raddr, 'port'):
                    if conn.raddr.port in suspicious_ports:
                        indicators.append(f"Connection to suspicious port {conn.raddr.port}")
            
            # Check 3: Process parent anomalies
            parent = process.parent()
            if parent:
                if parent.pid == 1 and process.name() not in ['systemd', 'init']:
                    indicators.append("Orphan process (parent is init)")
            
            # Check 4: Memory usage anomalies
            memory_mb = process.memory_info().rss / 1024 / 1024
            if memory_mb > 500:  # More than 500MB for unknown process
                if not any(sys_proc in process.name().lower() for sys_proc in ['chrome', 'firefox', 'java']):
                    indicators.append("High memory usage for process type")
        
        except Exception as e:
            indicators.append(f"Analysis limited: {e}")
        
        # Report findings
        if indicators:
            for indicator in indicators:
                print(f"  {Fore.RED}• {indicator}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}• No strong behavioral indicators detected{Style.RESET_ALL}")