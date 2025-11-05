#!/usr/bin/env python3
"""
BackdoorUpgrade - Simple backdoor detection tool
Author: Satayu47
"""

import argparse
import sys
import os
from core.detection.process_monitor import ProcessMonitor
from core.detection.network_analyzer import NetworkAnalyzer
from core.analysis.behavioral_analyzer import BehavioralAnalyzer

def display_banner():
    banner = """
    BackdoorUpgrade v1.0 - Simple Backdoor Detection
    ===============================================
    """
    print(banner)

def main():
    display_banner()
    
    parser = argparse.ArgumentParser(description='BackdoorUpgrade - Simple backdoor detection')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Detect command
    detect_parser = subparsers.add_parser('detect', help='Detection features')
    detect_parser.add_argument('--processes', action='store_true', help='Find suspicious processes')
    detect_parser.add_argument('--network', action='store_true', help='Analyze network connections')
    detect_parser.add_argument('--all', action='store_true', help='Run all detection methods')
    
    # Analyze command  
    analyze_parser = subparsers.add_parser('analyze', help='Analysis features')
    analyze_parser.add_argument('--pid', type=int, help='Analyze specific process ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'detect':
            if args.processes or args.all:
                print("\n[🔍] SCANNING PROCESSES...")
                monitor = ProcessMonitor()
                monitor.scan_suspicious_processes()
                
            if args.network or args.all:
                print("\n[🌐] ANALYZING NETWORK...")
                analyzer = NetworkAnalyzer()
                analyzer.analyze_connections()
                
        elif args.command == 'analyze':
            if args.pid:
                print(f"\n[🔬] ANALYZING PROCESS PID: {args.pid}")
                analyzer = BehavioralAnalyzer()
                analyzer.analyze_process(args.pid)
                
    except KeyboardInterrupt:
        print("\n[!] Stopped by user")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    main()