FUNCTION new_credentials_add (username,password,confirmpassword) returns bool
    if password != confirmpassword OR username.isempty() or password.isempty()
        return False
    endif 
    CONNECT to 'users.db'
    RUN SQL ''' select * from users where user like '{username}' '''
    if SQL returns entry then
        close CONNECT
        return false
    else 
        string var hash_password = ''
        hashed_password = FUNCTION hasher(password)
        RUN SQL ''' INSERT INTO users VALUES ('{username}','{hashed_password}')
        close CONNECT
        return true
    endif
endFUNCTION

FUNCTION login (username,password) returns bool 
    var string hashed_password = '' 
    hashed_password = FUNCTION hasher(password)
    CONNECT to 'users.db'
    RUN SQL ''' SELECT * FROM users WHERE username LIKE'{username}' AND password LIKE '{hashed_password}' '''
    if SQL returns RESULT then
        return True
    else 
        return False
    endif
endFUNCTION

FUNCTION hasher(password) returns string
    ENCODE password as ascii
    var str output = '' 
    output = hashlib.sha256(password)
    output = output.hexdigest()
    RETURN output
endFUNCTION


PROCEDURE startup() returns none
    #start with DB check
    if path users.db does not exist then
        CONNECT to 'users.db'
        RUN SQL ''' create table users (username TEXT,password TEXT)'''
        commmit SQL
        close CONNECT
    end if
    BOOL login = False
    while login = False do 
        start up START SCREEN UI
        UI CHOICE (SCREEN 1)
        MATCH choice
            CASE Login
                int var fail_count = 0 
                while fail_count < 5 do
                    LOGIN SCREEN UI
                    get username,password from UI
                    if FUNCTION login success then
                        login = True
                        exit while
                    else then
                        fail_count + 1
                    end if
                end while
                if login = False then
                    return [False] 
                endif
            CASE Signup
                UI SCREEN SIGNUP
                int var fail_count = 0
                while fail_count < 5 do
                    UI get username,password, confirmpassword
                    if FUNCTION new_credentials_add(username,password,confirmpassword) success then
                        exit while # will go back to start screen ui
                    else 
                        fail_count + 1
                    end if
                endwhile 
                if fail_count >=5 then 
                    return [False] 
                endif
        end MATCH
    endwhile
    return [True,(username,password)]
endPROCEDURE



PROCEDURE main() returns none
    VAR list startup_output = ''
    VAR bool login = False
    WHILE login = False do 
        startup_output = startup() #startup returns a list with a bool and a tuple, 
        if startup_output[0] = True then 
            login = True
        endif 
    endwhlie
    VAR tuple credentials = ()
    credentials = startup_output[1] 
    FUNCTION homepage(username = credentials[0],password = credentials[1])

endPROCEDURE
