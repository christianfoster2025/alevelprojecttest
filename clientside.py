
'''
# Import socket module
import socket

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 8008

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# receive data from the server
print(s.recv(1024))

# close the connection
s.close()
'''

import os
import re

def get_ip_from_mac(mac_address):
    # Get the ARP table
    arp_table = os.popen('arp -a').read()
    # Search for the MAC address in the ARP table
    for line in arp_table.splitlines():
        if mac_address.lower() in line.lower():
            # Extract the IP address
            ip_address = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
            if ip_address:
                return ip_address[0]
    return None

mac = '3C:7C:3F:22:DC:E2'  # Replace with the target MAC address
ip = get_ip_from_mac(mac)
print(f'IP Address: {ip}')