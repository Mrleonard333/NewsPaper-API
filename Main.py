from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import Functions
import jwt

System = FastAPI()                          # v The authentication token path
Auth_Sys = OAuth2PasswordBearer(tokenUrl="authentication") # < Will create a authentication bearer

class Get_Matter_Model(BaseModel): # < Will create a model for the json data
    About: str # < The variable is expected to be a string

class News_Model(BaseModel):
    Title: str
    Matter: str

class User_Model(BaseModel):
    Username: str
    Password: str

@System.post("/authentication")     # v Will request the user's information
async def Autenticate(Client_Info: OAuth2PasswordRequestForm = Depends()):
    Token = Functions.Token_Creation(Client_Info.username, Client_Info.password)
    if Token:
        return {"access_token":Token, "token_type":"bearer"}
    
    raise HTTPException(401, "Unregistered Journalist") # < Will send a Unauthorized status

@System.post("/create_a_user")
async def Create_a_User(User_Data: User_Model):
    if Functions.Create_New_User(User_Data.Username, User_Data.Password):
        return {"Result": "User Created"}
    
    return {"Result": "User already exists"}

@System.post("/create_a_matter")                            # v The function need the authentication token to start
async def Create_a_Matter(News: News_Model, Token: str = Depends(Auth_Sys)):
    if Functions.Verify_Token(Token):
        Id = 1
        Connection, Cursor = Functions.DataBase()
        INFO = Functions.Get_DataBase_Data(Connection, Cursor, Value="matter", Table="news_info")

                    # v Will get the token data
        User = jwt.decode(Token, "SECRET_KEY", algorithms=["Algorithm"])["User"]

        for I in INFO:
            Id += 1
            if News.Matter == I[0]:
                return {"Result": "Matter already exists"}
            
        Cursor.execute(f"INSERT INTO `news`.`news_info` (`id`, `title`, `matter`, `user`) VALUES ('{Id}', '{News.Title}', '{News.Matter}', '{User}');")
        Connection.commit()

        Cursor.close()
        Connection.close
        return {"Result": "News created"}
    
    return {"Result": "User not authenticated"}

@System.post("/matters")
async def Get_Matters(Matter: Get_Matter_Model):
    Matters_Info = dict()
    Connection, Cursor = Functions.DataBase()
    INFO = Functions.Get_DataBase_Data(Connection, Cursor, Value="*", Table="news_info")

    for I in INFO:                  # v Title                               # v Author
        if Matter.About.lower() in I[1].lower() or Matter.About.lower() in I[3].lower():
            try:
                Matters_Info["Matter"].append([I[1], I[2], I[3]])
            except:
                Matters_Info["Matter"] = [[I[1], I[2], I[3]]]

    if Matters_Info:
        return {"Result":Matters_Info}
    else:
        return {"Result":"No Matters Found"}