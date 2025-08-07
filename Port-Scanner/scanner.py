import sys
import socket


def is_valid_ipv4(ip: str):
	parts = ip.split(".")
	if len(parts) != 4:
		return False
	for part in parts:
		if not part.isdigit():
			return False
		num = int(part)
		# There must be no leading 0s (e.g. 01)
		if part != str(num):
			return False
		if num < 0 or num > 255:
			return False
	return True
	
	
def is_valid_port(port: str):
	if not port.isdigit():
		return False
	port = int(port)
	if port < 1 or port > 65535:
		return False
	return True
	
	
def get_scanning_ports(port_range):
	scan_ports = []
	ranges = port_range.split(",")
	for pr in ranges:
		ports = pr.split("-")
		if len(ports) == 1:
			port = ports[0]
			if not is_valid_port(port):
				return None
			scan_ports.append(int(port))
		elif len(ports) == 2:
			start, end = ports
			if not is_valid_port(start) or not is_valid_port(end):
				return None
			start, end = int(start), int(end)
			if start > end:
				return None
			scan_ports.extend(range(start, end + 1))
		else:
			return None
	return sorted(set(scan_ports))


print()
print("-" * 23, "Port Scanner", "-" * 23)
print()

ip = input("Enter the IPv4 address to scan: ").strip()
if not is_valid_ipv4(ip):
	raise ValueError(f"Invalid IPv4 address: {ip}")
	
port_range = input("Enter the range of ports to scan (e.g. 20-80,443): ").strip()
scan_ports = get_scanning_ports(port_range)
if scan_ports is None:
	raise ValueError(f"Invalid port range: {port_range}")

print("-" * 60)	
try:
	socket.setdefaulttimeout(0.5)
	open_ports = []
	for port in scan_ports:
		print(f"Scanning port {port}...")
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			result = s.connect_ex((ip, port))
			if result == 0:
				open_ports.append(port)
				print(f"*Port {port} is open*")
		
except KeyboardInterrupt:
	print("\nExiting program...")
	sys.exit()
	
except socket.error:
	print("Could not connect to server!")
	sys.exit()
	
print("-" * 60)
print(f"Open Ports: {len(open_ports)} ({','.join(str(port) for port in open_ports)})")
print("-" * 60)
print()
