from datetime import timedelta, datetime
from passlib.hash import bcrypt
import mysql.connector as MySQL
import jwt

def DataBase():
    Connection = MySQL.connect( # < Will start a connection with the DataBase
        host="localhost",
        user="user",
        password="password",
        database="schema"
    )
    Cursor = Connection.cursor() # < For DataBase commands
    return Connection, Cursor

def Get_DataBase_Data(Cursor, Value: str, Table: str):
    Cursor.execute(f"SELECT {Value} FROM news.{Table};") # < Will execute a SQL script
    INFO = Cursor.fetchall() # < Will get the DataBase info

    return INFO

def Token_Creation(Username: str, Password: str):
    Connection, Cursor = DataBase()
    INFO = Get_DataBase_Data(Connection, Cursor, Value="*", Table="creators")

    for I in INFO:                              # v Will verify the encrypted password
        if Username.lower() == I[1].lower() and bcrypt.verify(Password, I[2]):
                                                        # v Date and Time in UTC code
            Token_Info = {"User":Username, "exp":datetime.utcnow() + timedelta(minutes=30)}

                                # v The token dict          # v The encryption algorithm
            Token = jwt.encode(Token_Info, "SECRET_KEY", algorithm="Algorithm")  # < Will create the JWT token
                                            # ^ The key for encryption
            Cursor.close()
            Connection.close # < Will close the connection with the database
            return Token
    
    return False

def Verify_Token(Token: str):
    try:
        Token_Info = jwt.decode(Token, "SECRET_KEY", algorithms=["Algorithm"])
    except:
        return False
    
    Connection, Cursor = DataBase()
    INFO = Get_DataBase_Data(Connection, Cursor, Value="Username", Table="creators")

    for I in INFO:
        if Token_Info["User"].lower() == I[0].lower():
            Cursor.close()
            Connection.close
            return True

    Cursor.close()
    Connection.close
    return False

def Create_New_User(Username: str, Password: str):
    Id = 1
    Connection, Cursor = DataBase()
    INFO = Get_DataBase_Data(Connection, Cursor, Value="Username", Table="creators")

    for I in INFO:
        Id += 1
        if I[0] == Username:
            Cursor.close()
            Connection.close
            return False
    
    Hash_Pass = bcrypt.hash(Password) # < Will create a hash with the password
    Cursor.execute(f"INSERT INTO `news`.`creators` (`id`, `username`, `password`) VALUES ('{Id}', '{Username}', '{Hash_Pass}');")
    Connection.commit() # < Will save the DataBase changes

    Cursor.close()
    Connection.close
    return True