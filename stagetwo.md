```
required libraries: cryptography, socket, datetime

FUNCTION encryption(message, mode)
    return message
endFUNCTION

FUNCTION update_message_state(new_state)
    SQL CONNECT to 'programme.db'
    RUN SQL ''' UPDATE messages SET STATE = '{new_state}' where timestamp = (SELECT MAX(timestamp) FROM messages) '''
    CLOSE CONNECT
ENDFUNCTION

FUNCTION wifi_receive_message() -> returns message
    wifi_connection = socket.socket()
    connection_port = 8008 
    wifi_connection.bind(('',connection_port))
    wifi_connection.listen(5)    
    global var bool receive_running = True
    while receive_running do 







# finish this bit, need to update to database, consider making it its own function , add decrypt, add stuff for receiving read receipts, add bit in to go from local ip to mac address then look this up in contacts for sender in db record     
        # Establish connection with client.
        connection, address = wifilink.accept()
        #print ('Got connection from', addr )
        receivedmessage =str(c.recv(1024))
        
        print(f'{addr}: {receivedmessage[2:-1]}')
        # send a thank you message to the client.
        

        # Close the connection with the client
        c.close()
endFUNCTION




FUNCTION wifi_send_message(message:string,recipient:str,userID:str) -> returns bool
    CONNECT to 'programme.db'
    RUN SQL ''' SELECT wifi_mac_address FROM contacts WHERE contactID LIKE'{recipient}'; '''
    if SQL returns RESULT then
        mac_address = SQL RESULT
        CLOSE CONNECT
    else 
        CLOSE CONNECT
        return False
    endif

    arp_table = os.popen('arp -a').read()
    for line in arp_table.splitlines() do
        if mac_address.lower() in line.lower() OR mac_address.lower().replace(':','-') in line.lower() then
            ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
            if ip_match then
                ip_address = ip_match.group()
            else then
                return False
            endif
        else then
            return False
        endif
    endfor

    encrypted_message = encrypt(message,encrypt=True)
    var str timestamp = str(datetime.datetime.now()).split('.')[0]
    CONNECT to 'programme.db'
    RUN SQL ''' INSERT INTO messages VALUES ('{timestamp}','{userID}','{recipient}','{encrypted_message},'{purgatory})'''
    close CONNECT


    wifi_send_socket= socket.socket()
    var int wifi_port = 8008
    try do 
        wifi_send_socket.connect((ip_address, wifi_port))
        wifi_send_socket.send(encrypted_message)
        CLOSE wifi_send_socket
        FUNCTION update_message_state('sent')
        return True
    except ConnectionRefusedError:
        CLOSE wifi_send_socket
        return False
    ENDtry
ENDFUNCTION
```