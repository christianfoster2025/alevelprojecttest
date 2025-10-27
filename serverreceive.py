import socket
## TODO make alot better as per freeform spec


def receiver():
    wifilink = socket.socket()
    port = 8008
    wifilink.bind(('', port))
    print ("socket binded to %s" %(port))
    wifilink.listen(5)    
    print ("socket is listening")

    while True:
        # Establish connection with client.
        c, addr = wifilink.accept()
        #print ('Got connection from', addr )
        receivedmessage =str(c.recv(1024))
        
        print(f'{addr}: {receivedmessage[2:-1]}')
        # send a thank you message to the client.
        

        # Close the connection with the client
        c.close()


if __name__ == '__main__':
    receiver()