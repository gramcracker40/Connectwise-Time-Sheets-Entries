import requests, json
import env_var

charge_codes_req = requests.get(env_var.get_charge_codes, headers=env_var.cw_headers)
charge_codes = json.loads(charge_codes_req.text)

def get_charge_codes():
    charge_codes_name_id = {x['id']:x['name'] for x in charge_codes}
    return charge_codes_name_id

# test = get_charge_codes()
# print(test)