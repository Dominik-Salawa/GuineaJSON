import guineajson as G
import os
import random as R
addr = "info.json"
accounts = []

message = "Hello, Admin"

try:
    accounts = G.fetch(addr) # I want to catch the error
    message  = "Fetched the JSON!\nHello, Admin"
except Exception as e:
    message  = "Couldnt fetch JSON...\nHello, Admin"
    accounts = []

def id_exists(id):
    for account in accounts:
        if id == account["userid"]:
            return True
    return False

def generate_id():
    while True:
        id = R.randint(100000000000, 999999999999)
        if not id_exists(id): return id

while True:
    os.system("cls")
    print(message)
    message = ""
    print("Enter a cmd:")
    inp = input()
    if inp == "adduser":
        u = {"name": "", "userid": 0, "type": "", "balance": 0.0, "overdraft": False}

        # Getting name
        u["name"]       =       input("name   : ")
        while not len(u["name"]) > 0:
            print("INCORRECT INPUT! MUST BE GREATER THAN 0 CHAR LONG!")
            u["name"]       =       input("name   : ")

        # Getting account type
        u["type"]    =       input("type of account (savings|spending): ").upper()
        while not u["type"].lower() in ["savings", "spending"]:
            print("INCORRECT ACCOUNT TYPE!")
            u["type"] = input("type of account (savings|spending): ").upper()

        # Getting balance
        u["balance"]    = float(input("balance: £"))
        u["overdraft"]  = u["balance"] < 0
        
        u["userid"]     = generate_id()

        accounts.append(u)
        message = f"Account [{u["userid"]}] created"
    elif inp == "deluser":
        id = int(input("ID: "))

        found = False
        for account in accounts:
            if account["userid"] == id:
                found   = True
                accounts.remove(account)
                message = "Account deleted"
                break

        if not found:
            message = "ID does not exist!"
    elif inp == "view":
        # FINISH
        input()
    elif inp == "viewall":
        for account in accounts:
            print(("-" * 20) + "\n" + account["name"] + f" ({account["userid"]})\n" + ("-" * len(f"{account["name"]} ({account["userid"]})")) + "\nAccount Type:" + (" " * 2) + account["type"] + "\nBalance:" + (" " * 7) + "£" + str(account["balance"]) + "\nOverdraft:" + (" " * 5) + str(account["overdraft"]).upper())
        print("-" * 20)
        input()
    elif inp == "clearall":
        if input("Are you sure (Y/n)?: ") == "Y":
            accounts = []
            message = "Database wiped"
    elif inp == "exit":
        break

G.save(accounts, addr, True, True, True)