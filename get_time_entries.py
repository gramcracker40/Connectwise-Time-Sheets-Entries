from datetime import date
import requests
import json
import math
import env_var
from get_time_sheets import get_time_period, get_all_time_periods


def get_time_entries(periodStart, periodEnd):
    '''
    periodStart : must be a date object from datetime library
    periodEnd : must be a date object from datetime library

    gets all the time entries between a specific set of dates and returns them
        in a list

    '''

    #finding all the pages needed
    time_entries_count_req = requests.get(env_var.get_time_entries_count, 
                                          headers=env_var.cw_headers)
    time_entries_count = json.loads(time_entries_count_req.text)
    pages_needed = math.ceil(time_entries_count['count']/1000)

    period_time_entries = []
    #looping through the time entry pages
    for page in range(pages_needed):
        req_url = env_var.get_time_entries + f"&page={page + 1}"

        time_entries_req = requests.get(req_url, headers=env_var.cw_headers)
        time_entries = json.loads(time_entries_req.text)

        for each in time_entries:
            day = each['timeStart'].split('T')
            day = date.fromisoformat(day[0])

            if day >= periodStart and day <= periodEnd:
                period_time_entries.append(each)
            
    return period_time_entries





