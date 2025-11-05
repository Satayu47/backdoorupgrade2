# BackdoorUpgrade

A simple Python-based security tool for detecting suspicious processes and network activity. Built this during some late-night security research sessions.

## Features

- Process monitoring and detection
- Network connection analysis  
- Basic behavioral analysis
- Command-line interface
- Cross-platform support

## Requirements

- Python 3.6 or newer
- psutil and colorama libraries

## Installation & Usage

```bash
git clone https://github.com/Satayu47/backdoorupgrade2.git
cd backdoorupgrade2
pip install -r requirements.txt
```

Basic usage:
```bash
# Check processes
python backdoorupgrade.py detect --processes

# Check network connections  
python backdoorupgrade.py detect --network

# Run everything
python backdoorupgrade.py detect --all

# Analyze specific process
python backdoorupgrade.py analyze --pid <pid>
```

## How it works

The tool looks for common indicators of malicious activity:

**Process Detection:**
- Scans running processes for suspicious names
- Checks command line arguments for known bad keywords
- Identifies processes with unusual characteristics

**Network Analysis:**
- Monitors active connections
- Flags connections to commonly used backdoor ports
- Reports suspicious network activity

**Behavioral Analysis:**
- Examines process memory usage, threads, etc.
- Looks for parent/child process anomalies
- Checks for signs of code injection or hiding

## Detection signatures

Currently looks for these indicators:

**Suspicious processes:**
- nc, netcat variants (nc.exe, ncat, etc.)
- Common hacking tools (mimikatz, metasploit components)
- Reverse shell utilities
- Port scanners and network tools

**Suspicious ports:**
- 4444, 1337, 31337 (commonly used for backdoors)
- Other non-standard listening ports

**Behavioral red flags:**
- Processes with extremely high thread counts
- Orphaned processes (parent died)
- Processes consuming unusual amounts of memory

You can customize the detection rules by editing `config/signatures.json`.

## Notes

- False positives are possible, especially with legitimate security tools
- Some Windows system processes might trigger alerts due to access restrictions
- Run with admin/root privileges for better process information
- The tool is designed for educational and authorized testing only

## Why I built this

Started as a side project while learning about malware detection techniques. Wanted something lightweight that could quickly spot obvious signs of compromise without needing complex signatures or machine learning.

## Project structure

```
backdoorupgrade/
├── backdoorupgrade.py          # Main script
├── requirements.txt             # Dependencies  
├── core/
│   ├── detection/
│   │   ├── process_monitor.py  # Process scanning logic
│   │   └── network_analyzer.py # Network connection analysis
│   └── analysis/
│       └── behavioral_analyzer.py # Process behavior analysis
└── config/
    └── signatures.json         # Detection rules
```

## Dependencies

- psutil - for system/process information
- colorama - for colored terminal output

Both should install automatically with `pip install -r requirements.txt`.

## Disclaimer

This is for educational purposes and authorized testing only. Don't use this on systems you don't own or don't have permission to test.

## Troubleshooting

**Import errors:** Make sure you've installed the requirements with `pip install -r requirements.txt`

**Permission errors:** Try running with elevated privileges (admin on Windows, sudo on Linux/Mac)

**Lots of false positives:** This is normal on Windows due to system process restrictions. The tool errs on the side of caution.

## Contributing

Feel free to submit issues or pull requests if you find bugs or want to add features. Some ideas:
- Better signature detection
- Real-time monitoring mode  
- Export results to file
- GUI version

## License

MIT License - see LICENSE file for details.