import os, re, socket


contactlist  = { # temporary will need to be removed
  ...
}


def Contact2MAC() ->str:
    while True:
        print('choose who to send to from the following:')
        for contact in contactlist:
            print(contact)
        choice = input()
        if choice in contactlist:
            return contactlist[choice]

def MACtoIP(mac_address:str): #uses lookup table on device to find local ip of device wanted 
    # Get the ARP table
    arp_table = os.popen('arp -a').read()
    # Search for the MAC address in the ARP table
    for line in arp_table.splitlines():
        if mac_address.lower() in line.lower() or mac_address.lower().replace(':','-') in line.lower():
            # Extract the IP address
            ip_address = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
            if ip_address:
                return ip_address[0]
            
    return int(a) # need to fix

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
        return True
    except ConnectionRefusedError:
        print('client not online')
        return False
    

def sendscript(message:str,macaddress): # receiver has to be one of either homepc or macbook and message has to be a string TODO implement DB here
    ipaddress = MACtoIP(macaddress)
    message= message.encode('ascii')
    wifisendmodule(ipaddress,message)


#tester script


if __name__ == '__main__':
    macaddress= ''
    while True:
        print('choose who to send to from the following:')
        for contact in contactlist:
            print(contact)
        choice = input()
        if choice in contactlist:
            macaddress= contactlist[choice]
            break
        
    message = input('enter message:')
    sendscript(message, macaddress)
    


# script takes in mac address, 
# gets local ip

# then gets message
# encrypts 
#connects
#sends 
# closes

