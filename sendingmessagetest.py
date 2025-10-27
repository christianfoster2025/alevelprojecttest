# first of all import the socket library
import socket
## TODO make alot better as per freeform spec
def connect():
    wifilink = socket.socket()

    port = 8008
    try:
        # connect to the server on local computer
        wifilink.connect(('127.0.0.1', port))

        # receive data from the server
        print(wifilink.recv(1024))

        # close the connection
        wifilink.close()
    except ConnectionRefusedError:
        wifilink.bind(('', port))
        print ("socket binded to %s" %(port))
        s.listen(5)    
        print ("socket is listening")

        while True:
            # Establish connection with client.
            c, addr = s.accept()
            print ('Got connection from', addr )

            # send a thank you message to the client.
            c.send(b'Thank you for connecting')

            # Close the connection with the client
            c.close()
        
if __name__ == '__main__':
    connect()