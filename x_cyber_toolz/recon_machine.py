#!/usr/bin/env python3

import platform
import socket
import netifaces
import urllib.request
import psutil
from uuid import getnode
import requests
import json
from datetime import datetime

class SystemRecon:
    def __init__(self):
        self.data = {}
        self.collect_all_data()

    def get_mac_address(self):
        """Get MAC address in a cross-platform way"""
        mac = getnode()
        return ':'.join(('%012x' % mac)[i:i+2] for i in range(0, 12, 2))

    def get_public_ip(self):
        """Get public IP with error handling and timeout"""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            return response.json()['ip']
        except:
            try:
                # Fallback method
                return urllib.request.urlopen('https://ident.me', timeout=5).read().decode('utf8')
            except:
                return "Unable to determine public IP"

    def get_network_info(self):
        """Collect network information"""
        network_info = {
            'hostname': socket.gethostname(),
            'local_ip': socket.gethostbyname(socket.gethostname()),
            'public_ip': self.get_public_ip(),
            'mac_address': self.get_mac_address(),
            'interfaces': {}
        }

        # Collect information for all network interfaces
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            interface_info = {}
            
            # Get IPv4 information
            if netifaces.AF_INET in addrs:
                ipv4_info = addrs[netifaces.AF_INET][0]
                if ipv4_info.get('addr') != '127.0.0.1':
                    interface_info['ipv4'] = {
                        'address': ipv4_info.get('addr'),
                        'netmask': ipv4_info.get('netmask'),
                        'broadcast': ipv4_info.get('broadcast')
                    }
            
            # Get IPv6 information
            if netifaces.AF_INET6 in addrs:
                ipv6_addresses = []
                for addr in addrs[netifaces.AF_INET6]:
                    if '%' not in addr['addr']:  # Filter out link-local addresses
                        ipv6_addresses.append(addr['addr'])
                if ipv6_addresses:
                    interface_info['ipv6'] = ipv6_addresses

            if interface_info:  # Only add interfaces with IP information
                network_info['interfaces'][iface] = interface_info

        return network_info

    def get_system_info(self):
        """Collect system information"""
        return {
            'os_name': platform.system(),
            'os_release': platform.release(),
            'os_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version()
        }

    def get_hardware_info(self):
        """Collect hardware information"""
        cpu_freq = psutil.cpu_freq()
        return {
            'cpu': {
                'physical_cores': psutil.cpu_count(logical=False),
                'total_cores': psutil.cpu_count(logical=True),
                'max_frequency': cpu_freq.max if cpu_freq else 'N/A',
                'min_frequency': cpu_freq.min if cpu_freq else 'N/A',
                'current_frequency': cpu_freq.current if cpu_freq else 'N/A',
                'usage_per_core': psutil.cpu_percent(percpu=True),
                'total_usage': psutil.cpu_percent()
            },
            'memory': {
                'total': round(psutil.virtual_memory().total / (1024**3), 2),
                'available': round(psutil.virtual_memory().available / (1024**3), 2),
                'used': round(psutil.virtual_memory().used / (1024**3), 2),
                'percentage': psutil.virtual_memory().percent
            },
            'disk': self.get_disk_info()
        }

    def get_disk_info(self):
        """Collect disk information"""
        disk_info = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.mountpoint] = {
                    'device': partition.device,
                    'fstype': partition.fstype,
                    'total': round(usage.total / (1024**3), 2),
                    'used': round(usage.used / (1024**3), 2),
                    'free': round(usage.free / (1024**3), 2),
                    'percentage': usage.percent
                }
            except PermissionError:
                continue
        return disk_info

    def collect_all_data(self):
        """Collect all system information"""
        self.data = {
            'timestamp': datetime.now().isoformat(),
            'network': self.get_network_info(),
            'system': self.get_system_info(),
            'hardware': self.get_hardware_info()
        }

    def generate_report(self, format='text'):
        """Generate a report in the specified format"""
        if format == 'json':
            return json.dumps(self.data, indent=4)
        else:
            # Text format
            report = []
            report.append("=== System Reconnaissance Report ===")
            report.append(f"Generated at: {self.data['timestamp']}\n")
            
            # Network Information
            report.append("=== Network Information ===")
            net = self.data['network']
            report.append(f"Hostname: {net['hostname']}")
            report.append(f"Local IP: {net['local_ip']}")
            report.append(f"Public IP: {net['public_ip']}")
            report.append(f"MAC Address: {net['mac_address']}")
            
            for iface, info in net['interfaces'].items():
                report.append(f"\nInterface: {iface}")
                if 'ipv4' in info:
                    report.append(f"  IPv4 Address: {info['ipv4']['address']}")
                    report.append(f"  Netmask: {info['ipv4']['netmask']}")
                    report.append(f"  Broadcast: {info['ipv4']['broadcast']}")
                if 'ipv6' in info:
                    for addr in info['ipv6']:
                        report.append(f"  IPv6 Address: {addr}")

            # System Information
            report.append("\n=== System Information ===")
            sys = self.data['system']
            report.append(f"OS: {sys['os_name']} {sys['os_release']}")
            report.append(f"OS Version: {sys['os_version']}")
            report.append(f"Architecture: {sys['architecture']}")
            report.append(f"Processor: {sys['processor']}")
            report.append(f"Python Version: {sys['python_version']}")

            # Hardware Information
            report.append("\n=== Hardware Information ===")
            hw = self.data['hardware']
            report.append(f"CPU Physical Cores: {hw['cpu']['physical_cores']}")
            report.append(f"CPU Total Cores: {hw['cpu']['total_cores']}")
            report.append(f"CPU Current Frequency: {hw['cpu']['current_frequency']} MHz")
            report.append(f"CPU Usage: {hw['cpu']['total_usage']}%")
            
            report.append(f"\nMemory Total: {hw['memory']['total']} GB")
            report.append(f"Memory Available: {hw['memory']['available']} GB")
            report.append(f"Memory Used: {hw['memory']['used']} GB")
            report.append(f"Memory Usage: {hw['memory']['percentage']}%")

            report.append("\n=== Disk Information ===")
            for mount, disk in hw['disk'].items():
                report.append(f"\nMount Point: {mount}")
                report.append(f"  Device: {disk['device']}")
                report.append(f"  Filesystem: {disk['fstype']}")
                report.append(f"  Total: {disk['total']} GB")
                report.append(f"  Used: {disk['used']} GB")
                report.append(f"  Free: {disk['free']} GB")
                report.append(f"  Usage: {disk['percentage']}%")

            return '\n'.join(report)

def main():
    recon = SystemRecon()
    
    # Generate both text and JSON reports
    print(recon.generate_report('text'))
    
    # Save JSON report to file
    with open(f'system_recon_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
        f.write(recon.generate_report('json'))

if __name__ == "__main__":
    main()