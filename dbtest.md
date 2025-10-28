FUNCTION new_credentials_add (username,password,confirmpassowrd) returns bool
    INPUT username
    INPUT password
    INPUT confirmpassword
    if password != confirmpassword OR username.isempty() or password.isempty()
        return False
    endif 
    CONNECT to 'users.db'
    RUN SQL ''' select * from 'users.db' where user like username '''
    if SQL returns entry then
        close CONNECT
        return false
    else 
        RUN SQL ''' INSERT INTO users VALUES (username,password)
        close CONNECTR
        return true
    endif


PROCEDURE startup() returns none
    #start with DB check
    if path users.db exists then
        continue
    else 
        CONNECT to 'users.db'
        RUN SQL ''' create table users (username test,password,text)'''
        commmit SQL
        close CONNECT
    end if
    start up START SCREEN UI
    UI CHOICE (SCREEN 1)
    MATCH choice
        CASE Login
            int fail_count = 0 
            while fail_count < 5 do
                LOGIN SCREEN UI
                get username,password from UI
                if FUNCTION login success then
                    FUNCTION homepage(username,password)
                else then
                    fail_count + 1
                end if
            end while 
            PROGRAMME EXIT #failed too many times 
        CASE Signup
            UI SCREEN
