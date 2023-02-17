import requests, json
import env_var

users_req = requests.get(env_var.get_cw_members, headers=env_var.cw_headers)
users = json.loads(users_req.text)

def get_users_id_name():
    id_name = {}
    for user in users:
        try:
            id_name[f"{user['firstName']} {user['lastName']}"] = user['id']
        except KeyError:
            pass


    return id_name

def get_users_name_id():
    id_name = {}
    for user in users:
        try:
            id_name[f"{user['firstName']} {user['lastName']}"] = user['id']
        except KeyError:
            pass


# test = get_users_id_name()
# print(test)