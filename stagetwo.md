```
required libraries: cryptography, socket, datetime

FUNCTION encryption(message,mode, recipient)  # mode can equal encrypt or decrypt, if recipient self then own private key used to decrypt, if a contacts details are given then it is known to be outbound and will be encrypted with their public key
'''
    MATCH mode
        CASE 'encrypt' then # outbound so encrypt with recipients public key
            CONNECT to 'programme.db'
            RUN SQL ''' SELECT public_key FROM contacts WHERE contactID LIKE'{recipient}'; '''
            if SQL returns RESULT then
                public_key = SQL RESULT
                CLOSE CONNECT
            else 
                CLOSE CONNECT
                return False
            endif
'''
#to be implemented if have time
    return message
endFUNCTION

FUNCTION update_message_state(new_state)
    SQL CONNECT to 'programme.db'
    RUN SQL ''' UPDATE messages SET STATE = '{new_state}' where timestamp = (SELECT MAX(timestamp) FROM messages) '''
    CLOSE CONNECT
ENDFUNCTION

FUNCTION wifi_receive_message(userID) -> returns message
    wifi_connection = socket.socket()
    connection_port = 8008 
    wifi_connection.bind(('',connection_port))
    wifi_connection.listen(5)    
    global var bool receive_running = True
    while receive_running do 
        receive_connection, sender = wifi_connection.accept()

        received_message =str(receive_connection.recv(1024))
        sender = arp_lookup(sender,'ip_2_mac')
        decrypted_message = FUNCTION encryption(received_message,'decrypt',userID)
        var str timestamp = str(datetime.datetime.now()).split('.')[0]

        CONNECT to 'programme.db'
        RUN SQL ''' INSERT INTO messages VALUES ('{timestamp}','{sender}','{userID}','{decrypted_message}','received')'''
        close CONNECT

        receive_connection.send(b'read')

        receive_connection.close()
endFUNCTION

FUNCTION arp_lookup(address,mode) #mode is either mac_2_ip or ip_2_mac
    arp_table = os.popen('arp -a').read()
    match mode 
        case 'mac_2_ip':
            for line in arp_table.splitlines() do
                if address.lower() in line.lower() OR address.lower().replace(':','-') in line.lower() then
                    ip_address = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
                    if ip_address then
                        ip_address = ip_address[0].decode('utf-8')
                        return ip_address
                    endif
                endif
            endfor
            return False
        case 'ip_2_mac':
            for line in arp_table.splitlines() do
                if address in line.lower() then
                    mac_address = re.findall(r'(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}', line)
                    if mac_address then
                        mac_address = str(mac_address[0]).replace('-',':')
                        return mac_address
                    endif
                endif
            endfor
            return False
    ENDMATCH
ENDFUNCTION

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

    ip_address = FUNCTION arp_lookup(mac_address, 'mac_2_ip')
    if ip_address == False then
        return false
    endif
    

    encrypted_message = encryption(message,recipient)
    var str timestamp = str(datetime.datetime.now()).split('.')[0]
    CONNECT to 'programme.db'
    RUN SQL ''' INSERT INTO messages VALUES ('{timestamp}','{userID}','{recipient}','{encrypted_message}','purgatory')'''
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