<p>FUNCTION sign_up (username,password,confirmpassword) returns bool</p>
<p>     if password != confirmpassword OR username.isempty() or password.isempty()</p>
<p>          return False</p>
<p>     endif </p>
<p>     CONNECT to 'users.db'</p>
<p>     RUN SQL ''' select * from users where username like '{username}' '''</p>
<p>     if SQL returns entry then</p>
<p>          close CONNECT</p>
<p>          return false</p>
<p>     else </p>
<p>          string var hash_password = ''</p>
<p>          hashed_password = FUNCTION hasher(password)</p>
<p>          RUN SQL ''' INSERT INTO users VALUES ('{username}','{hashed_password}')'''</p>
<p>          close CONNECT</p>
<p>          return true</p>
<p>     endif</p>
<p>endFUNCTION</p>
<p></p>
<p>FUNCTION login (username,password) returns bool </p>
<p>     var string hashed_password = '' </p>
<p>     hashed_password = FUNCTION hasher(password)</p>
<p>     CONNECT to 'users.db'</p>
<p>     RUN SQL ''' SELECT * FROM users WHERE username LIKE'{username}' AND password LIKE '{hashed_password}' '''</p>
<p>     if SQL returns RESULT then</p>
<p>          CLOSE CONNECT</p>
<p>          return True</p>
<p>     else </p>
<p>          CLOSE CONNECT</p>
<p>          return False</p>
<p>     endif</p>
<p>endFUNCTION</p>
<p></p>
<p>FUNCTION hasher(password) returns string</p>
<p>     ENCODE password as ascii</p>
<p>     var str output = '' </p>
<p>     output = hashlib.sha256(password)</p>
<p>     output = output.hexdigest()</p>
<p>     RETURN output</p>
<p>endFUNCTION</p>
<p></p>
<p></p>
<p>FUNCTION startup() returns list</p>
<p>     #start with DB check</p>
<p>     if path users.db does not exist then</p>
<p>          CONNECT to 'users.db'</p>
<p>          RUN SQL ''' create table users (username TEXT,password TEXT)'''</p>
<p>          commmit SQL</p>
<p>          close CONNECT</p>
<p>     end if</p>
<p>     BOOL login = False</p>
<p>     while login = False do </p>
<p>          start up START SCREEN UI</p>
<p>          UI CHOICE (SCREEN 1)</p>
<p>          MATCH choice</p>
<p>                CASE Login</p>
<p>                     int var fail_count = 0 </p>
<p>                     while fail_count < 5 do</p>
<p>                          LOGIN SCREEN UI</p>
<p>                          get username,password from UI</p>
<p>                          if FUNCTION login success then</p>
<p>                                login = True</p>
<p>                                exit while</p>
<p>                          else then</p>
<p>                                fail_count + 1</p>
<p>                          end if</p>
<p>                     end while</p>
<p>                     if login = False then</p>
<p>                          return [False] </p>
<p>                     endif</p>
<p>                CASE Signup</p>
<p>                     UI SCREEN SIGNUP</p>
<p>                     int var fail_count = 0</p>
<p>                     while fail_count < 5 do</p>
<p>                          UI get username,password, confirmpassword</p>
<p>                          if FUNCTION sign_up(username,password,confirmpassword) success then</p>
<p>                                exit while # will go back to start screen ui</p>
<p>                          else </p>
<p>                                fail_count + 1</p>
<p>                          end if</p>
<p>                     endwhile </p>
<p>                     if fail_count >=5 then </p>
<p>                          return [False] </p>
<p>                     endif</p>
<p>          end MATCH</p>
<p>     endwhile</p>
<p>     return [True,(username,password)]</p>
<p>endFUNCTION</p>
<p></p>
<p></p>
<p></p>
<p>PROCEDURE main() returns none</p>
<p>     VAR list startup_output = ''</p>
<p>     VAR bool login = False</p>
<p>     WHILE login = False do </p>
<p>          startup_output = FUNCTION startup() #startup returns a list with a bool and a tuple, </p>
<p>          if startup_output[0] = True then </p>
<p>                login = True</p>
<p>          endif </p>
<p>     endwhlie</p>
<p>     VAR tuple credentials = ()</p>
<p>     credentials = startup_output[1] </p>
<p>     FUNCTION homepage(username = credentials[0],password = credentials[1])</p>
<p></p>
<p>endPROCEDURE</p>
