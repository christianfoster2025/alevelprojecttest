import os
import re
import socket

contactlist  = {
  ...
}


def macchooserfromcontacts() ->str:
    while True:
        print('choose who to send to from the following:')
        for contact in contactlist:
            print(contact)
        choice = input()
        if choice in contactlist:
            return contactlist[choice]

def get_ip_from_mac(mac_address:str):
    # Get the ARP table
    arp_table = os.popen('arp -a').read()
    # Search for the MAC address in the ARP table
    for line in arp_table.splitlines():
        if mac_address.lower() in line.lower() or mac_address.lower().replace(':','-') in line.lower():
            # Extract the IP address
            ip_address = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
            if ip_address:
                print(ip_address[0])
                return ip_address[0]
            
    return int(a)

def fromcontacttolocalip(): 
    macaddress = macchooserfromcontacts()
    ip = get_ip_from_mac(macaddress)
    return str(ip)

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

def sendscript(message,receiver): # receiver has to be one of either homepc or macbook and message has to be a string 
    ipaddress = get_ip_from_mac(contactlist[receiver])
    wifisendmodule(ipaddress,message)


if __name__ == '__main__':
    message = input('input message:').encode('ascii') #needs and endwith''
    ip = fromcontacttolocalip()
    wifisendmodule(ip,message)