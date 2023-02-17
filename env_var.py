import requests
import json
import base64
from dotenv import dotenv_values

config = dotenv_values(".env")

# CW instance info
cw_id = config["CW_ID"]
cw_url = config["CW_URL"]

# Linking current connectwise codebase to the module
codebase_req = requests.get(f"https://{cw_url}/login/companyinfo/{cw_id}")
codebase_obj = json.loads(codebase_req.text)
accept_codebase = codebase_obj['VersionCode'].strip('v')

cw_base_url = f"https://{cw_url}/{codebase_obj['Codebase']}apis/3.0"

# CW credentials
clientId = config["CW_CLIENT_ID"]
cw_public = config["CW_PUBLIC"]
cw_private = config["CW_PRIVATE"]

# Packaging authentication headers {cw_id}
authorization_key = base64.b64encode(bytes(f"{cw_id}+{cw_public}:{cw_private}", 'utf-8'))

cw_headers = {
    "clientId": clientId,
    "Authorization":f"Basic {authorization_key.decode()}",
    "Accept": f"application/vnd.connectwise.com+json; version={accept_codebase}"
}

# CW Routes
get_time_sheets = cw_base_url + "/time/sheets?pageSize=1000"
get_time_sheets_count = cw_base_url + "/time/sheets/count"
time_period_setup = cw_base_url + "/time/timePeriodSetups?pageSize=1000"
get_time_entries = cw_base_url + "/time/entries?pageSize=1000"
get_time_entries_count = cw_base_url + "/time/entries/count"
get_cw_members = cw_base_url + "/system/members?pageSize=1000"
get_charge_codes = cw_base_url + "/time/chargeCodes?pageSize=1000"
