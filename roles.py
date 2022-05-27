import pickle
import cloudinary, urllib
import sys

ROLE_FILE = "Roles.pickle"

#Internal function for loading and returning the contents of the roles file
def load_roles():
    try:
        web_copy = cloudinary.api.resource(ROLE_FILE, resource_type='raw')['url']
        response = urllib.request.urlopen(web_copy)
        print(response)
        roleReact_db = pickle.load(response)
    except Exception as e:
        print(e)
        roleReact_db = {}

    with open(ROLE_FILE, "wb") as file:
            file.seek(0)
            pickle.dump(roleReact_db, file)

    return roleReact_db

def add_role(messageID, reaction, role):
    roleReact_db = load_roles() 
    if not roleReact_db:
        roleReact_db = {}

    if messageID not in roleReact_db:
        bar = {messageID: {reaction: role}}
        roleReact_db.update(bar)

    with open(ROLE_FILE, "wb") as file:
        roleReact_db[messageID][reaction] = role
        pickle.dump(roleReact_db, file)

    cloudinary.uploader.upload(ROLE_FILE, resource_type='raw', public_id=ROLE_FILE, invalidate=True)

def delete_reaction_role(messageID, reaction):
    roleReact_db = load_roles()
    if not roleReact_db:
        return("There are no role reactions set")

    if reaction == "ALL" and messageID in roleReact_db:
        roleReact_db.pop(messageID)

    elif messageID in roleReact_db and reaction in roleReact_db[messageID]:
        roleReact_db[messageID].pop(reaction)

    else:
        return(f"{reaction} reaction for {messageID} is not in database")

    with open(ROLE_FILE, "wb") as file:
        pickle.dump(roleReact_db, file)

    cloudinary.uploader.upload(ROLE_FILE, resource_type='raw', public_id=ROLE_FILE, invalidate=True)
    return("Done")

#Internal function for checking database for reaction based roles
def find_role(messageID, reaction):
    roleReact_db = load_roles()
    if messageID in roleReact_db:
        if reaction in roleReact_db[messageID]:
            return roleReact_db[messageID][reaction]

        else:
            print(f"{reaction} not in {messageID}")
            return None
    else:
        print(f"messageID {messageID} not found")
        return None
