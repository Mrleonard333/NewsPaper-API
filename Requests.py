from datetime import timedelta, datetime
from time import sleep
from os import system
import requests
import json
import jwt

def Clear():
    system("cls")
    system("clear")

Clear()

print("[NewsPaper-System]")
sleep(1)
print("Please identify yourself\n")
sleep(1)
print("[1] I have a account")
sleep(0.5)
print("[2] I need to register\n")
sleep(1)
Choise = int(input("[1/2] Choose one: "))

Clear()

print("[Fill the inputs]\n")
sleep(0.5)
Username = str(input("Username: "))
Password = str(input("Password: "))

if Choise == 2:
        Result = json.loads(requests.post("http://localhost:8000/create_a_user", json={"Username":Username, "Password":Password}).content.decode())

        if Result["Result"] == "User Created":
            print("\nYour account has been cadastraded")
            sleep(1)
            print("Now you can create your own news about any matter.")
            sleep(3.5)
        else:
            print("\nSomething is wrong")
            sleep(0.5)
            print("This account already exists")
            exit() # < Will end the execution
Token = jwt.encode({"User":Username, "exp":datetime.utcnow() + timedelta(minutes=30)}, "SECRET_KEY", algorithm="Algorithm")

Clear()

print("[What do you want to do?]\n")
sleep(0.5)
print("[1] Create my own news")
sleep(0.5)
print("[2] See created news\n")
sleep(1)
Choice = int(input("[1/2] Choose one: "))

Clear()

if Choice == 1:
    print("[Create your news]")
    print("User <B> in the matter to break the line\n")

    Title = str(input("Title: "))
    Matter = str(input("Matter: "))

    Response = json.loads(requests.post( # < Will send a POST method request
        url="http://localhost:8000/create_a_matter", # < The API path
        json={"Title":Title, "Matter":Matter}, # < Will send the require information in json
        headers={"Authorization": f"Bearer {Token}"} # < Will send the authentication token
    ).content.decode()) # < Will get the API content in a dict

    if Response["Result"] == "News created":
        print("\nThe news has been created")

    elif Response["Result"] == "Matter already exists":
        print("\nSomething is wrong")
        sleep(0.5)
        print(Response["Result"])
    
    else:
        print("\nYou need to have a account on the system")

elif Choice == 2:
    print("[What news do you want to see?]\n")
    sleep(0.5)
    About = str(input("About: "))

    Matters = json.loads(requests.post(
            url="http://localhost:8000/matters",
            json={"About":About}
    ).content.decode())["Result"]

    Clear()

    if Matters != "No Matters Found":
        Common_Matter = list()
        User_Matter = list()

        for M in Matters["Matter"]:
            if M[2].lower() == Username.lower():
                User_Matter.append(M)
            else:
                Common_Matter.append(M)

        if len(Common_Matter) >= 1:
            print("[Here is the results]\n")
            sleep(0.5)

            for Common_Info in Common_Matter:
                print("="*len(Common_Info[0]))
                print(Common_Info[0].upper())
                print("="*len(Common_Info[0]))

                print(Common_Info[1].replace("<B>", "\n"))
                
                print("="*int(len(Common_Info[2])) + 8)
                print(f"Author: {Common_Info[2]}\n")

        if len(User_Matter) >= 1:
            sleep(1)
            print("[Here is your matters about that]\n")
            sleep(0.5)

            for User_Info in User_Matter:
                print("="*len(User_Info[0]))
                print(User_Info[0].upper())
                print("="*len(User_Info[0]))

                print(User_Info[1].replace("<B>", "\n"), "\n")
    else:
        print("[Nothing about this was found]")