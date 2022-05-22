import pickle
import sys

ROLE_FILE = "Roles.pickle"

#Internal function for reading and returning the contents of the roles file
def read_roles():
    try:
        open(ROLE_FILE, "rb")
    except (FileNotFoundError, IOError):
        open(ROLE_FILE, "wb")

    finally:
        with open(ROLE_FILE, "rb") as file:
            if file.read(1):
                file.seek(0)
                db = pickle.load(file)
                return db

def add_role(messageID, reaction, role):
    roleReact_db = read_roles() 
    if not roleReact_db:
        roleReact_db = {}

    if messageID not in roleReact_db:
        bar = {messageID: {reaction: role}}
        roleReact_db.update(bar)

    with open(ROLE_FILE, "wb") as file:
        roleReact_db[messageID][reaction] = role
        pickle.dump(roleReact_db, file)
        print(roleReact_db)

def delete_role(messageID, reaction):
    roleReact_db = read_roles()
    if not roleReact_db:
        print("file is empty")
        return

    if reaction == "ALL" and messageID in roleReact_db:
        roleReact_db.pop(messageID)

    elif messageID in roleReact_db and reaction in roleReact_db[messageID]:
        roleReact_db[messageID].pop(reaction)

    else:
        return(f"{reaction} reaction for {messageID} is not in database")

    with open(ROLE_FILE, "wb") as file:
        pickle.dump(roleReact_db, file)
        print(roleReact_db)
        return("Done")

#Internal function for checking database for reaction based roles
def find_role(messageID, reaction):
    roleReact_db = read_roles()
    if messageID in roleReact_db:
        if reaction in roleReact_db[messageID]:
            return roleReact_db[messageID][reaction]

        else:
            print(f"{reaction} not in {messageID}")
            return None
    else:
        print(f"messageID {messageID} not found")
        return None
