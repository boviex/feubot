import pickle
import cloudinary, urllib
import sys

ROLE_FILE = "Roles.pickle"
MESSAGE_PROPERTIES_FILE = "MessageProperties.pickle"

#Internal function for loading and returning the contents of the roles file
def load_roles():
    try:
        web_copy = cloudinary.api.resource(ROLE_FILE, resource_type='raw')['url']
        response = urllib.request.urlopen(web_copy)
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
        temp = {messageID: {reaction: role}}
        roleReact_db.update(temp)

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

def load_properties():
    try:
        web_copy = cloudinary.api.resource(MESSAGE_PROPERTIES_FILE, resource_type='raw')['url']
        response = urllib.request.urlopen(web_copy)
        property_db = pickle.load(response)
    except Exception as e:
        print(e)
        property_db = {}

    with open(MESSAGE_PROPERTIES_FILE, "wb") as file:
            file.seek(0)
            pickle.dump(property_db, file)

    return property_db

def add_property(messageID, newProperty):
    property_db = load_properties()
    if not property_db:
        property_db = {}

    if messageID not in property_db:
        temp = {messageID: {newProperty: True}}
        property_db.update(temp)

    #Write data
    with open(MESSAGE_PROPERTIES_FILE, "wb") as file:
        property_db[messageID][newProperty] = True
        pickle.dump(property_db, file)

    cloudinary.uploader.upload(MESSAGE_PROPERTIES_FILE, resource_type='raw', public_id=MESSAGE_PROPERTIES_FILE, invalidate=True)

def delete_property(messageID, newProperty):
    property_db = load_properties()
    if not property_db:
        return("There are no message properties set")

    if newProperty == "ALL" and messageID in property_db:
        property_db.pop(messageID)

    elif messageID in property_db and newProperty in property_db[messageID]:
       property_db[messageID].pop(newProperty)

    else:
        return(f"{newProperty} property for {messageID} is not in database")

    #Write data
    with open(MESSAGE_PROPERTIES_FILE, "wb") as file:
        pickle.dump(property_db, file)

    cloudinary.uploader.upload(MESSAGE_PROPERTIES_FILE, resource_type='raw', public_id=MESSAGE_PROPERTIES_FILE, invalidate=True)
    return("Done")

def get_properties(messageID):
    property_db = load_properties()
    if messageID in property_db:
        return property_db[messageID]

    else:
        print(f"messageID {messageID} not found")
        return {}