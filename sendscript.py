
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

contactlist  = {
    'homepc': '3C:7C:3F:22:DC:E2',
    'macbook': 'ac:07:75:09:48:67'
}

import os
import re
import socket

def macchooserfromcontacts() ->str:
    while True:
        print('choose who to send to from the following:')
        for contact in contactlist:
            print(contact)
        choice = input()
        if choice in contactlist:
            return contactlist[choice]

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

def fromcontacttolocalip():
    macaddress = macchooserfromcontacts()
    ip = get_ip_from_mac(macaddress)
    return ip

def wifisendmodule(ipaddress, message):
    wifilink = socket.socket()

    port = 8008
    try:
        # connect to the server on local computer
        wifilink.connect((ipaddress, port))
        wifilink.send(message)
        # receive data from the server
        #print(wifilink.recv(1024))

        # close the connection
        wifilink.close()
        print('sent')
    except ConnectionRefusedError:
        print('client not online')


if __name__ == '__main___':
    message = input('input message:',end='')
    ip = fromcontacttolocalip()
    wifisendmodule(ip,message)