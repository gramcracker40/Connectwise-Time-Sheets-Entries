import requests
import json
import env_var
from datetime import date
import math

class TimeSheet:
    def __init__(self, timesheetID, employee, period, dateStart, dateEnd, status, hours):
        self.timesheetID = timesheetID
        self.employee = employee
        self.period = period
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.status = status
        self.hours = hours

    def __str__(self):
        return f"""
            Timesheet ID: {self.timesheetID},
            Employee Name: {self.employee},
            Period: {self.period},
            Date Start: {self.dateStart},
            Date End: {self.dateEnd},
            Status: {self.status}, 
            Hours: {self.hours}
        """

def get_all_timesheets(period):
    '''
    returns a list of all timesheets in a specific 'period' passed through
    
    Automatically grabs the current year and compares the timesheets year
        ensuring the timesheet is from the current timePeriodSetup
        allowing for this script to run indefinitely
    '''

    #grabbing the total count of timesheets in CW
    time_sheet_count_req = requests.get(env_var.get_time_sheets_count, headers=env_var.cw_headers)
    time_sheet_count = json.loads(time_sheet_count_req.text)
    pages_needed = math.ceil(time_sheet_count['count']/1000)
    
    curr_year = date.today().year

    #looping through all the seperate page requests and adding them to all_timesheets based
    # on year and period
    all_timesheets = []
    for page in range(pages_needed):
        req_url = env_var.get_time_sheets + f"&page={page + 1}"
        #Grabbing all timesheets from CW
        time_sheets_req = requests.get(req_url, headers=env_var.cw_headers)
        time_sheets = json.loads(time_sheets_req.text)

        for timesheet in time_sheets:
            if timesheet['period'] == period and curr_year == timesheet['year']:
                new_timesheet = TimeSheet(timesheet['id'], timesheet['member']['name'], 
                                timesheet['period'], timesheet['dateStart'], timesheet['dateEnd'], 
                                timesheet['status'], timesheet['hours'])
                all_timesheets.append(new_timesheet)
    

    return all_timesheets


def get_correct_time_sheet_id():
    '''
    helper function for below
    '''
    req = requests.get(env_var.time_period_setup, headers=env_var.cw_headers)
    time_period_setups = json.loads(req.text)

    curr_year = date.today().year
    time_sheet_id = 0

    for setup in time_period_setups:
        if setup['year'] == curr_year:
            time_sheet_id = setup['id']

    return time_sheet_id


### Running requests before the function call in case of multiple calls for get_time_period()
current_timesheet_id = get_correct_time_sheet_id()
timesheet_url = env_var.cw_base_url + f"/time/timePeriodSetups/{current_timesheet_id}/periods?pageSize=1000"
req = requests.get(timesheet_url, headers=env_var.cw_headers)
time_periods = json.loads(req.text)

def get_time_period(current_date):
    '''
    current_date: must be a date object from datetime library

    Grabs all of the most current 

    extension of get_correct_sheet_id(), grabs the current time period based on the 
        current_date that was passed through
    '''
  
    actual_period = 0
    for period in time_periods:
        period_start = date.fromisoformat(period['startDate'])
        period_end = date.fromisoformat(period['endDate'])

        if current_date >= period_start and current_date <= period_end:
            actual_period = period['period']
            break

    return actual_period


def get_all_time_periods():
    '''
    grabs a dictionary that gives the start and end date of each period(KEY)
    '''
    periods = {}
    for period in time_periods:
        periods[period['period']] = {
            'startDate': period['startDate'], 
            'endDate': period['endDate']
        }

    return periods
