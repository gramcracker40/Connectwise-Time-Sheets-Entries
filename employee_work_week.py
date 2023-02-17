from get_time_entries import get_time_entries
from get_time_sheets import get_all_timesheets, get_time_period
from get_charge_codes import get_charge_codes
from get_cw_users import get_users_id_name
from datetime import date

class EmployeeTimeRecord:
    def __init__(self, employee_name, employee_id):
        self.employee_name = employee_name
        self.employee_id = employee_id
        self.time_entries = []
        self.time_sheet = None

    def __repr__(self):
        return str({
            "employee": self.employee_name, 
            "employee_id": self.employee_id,
            "time_sheet": self.time_sheet,
            "time_entries": self.time_entries
        })


    def add_time_entry(self, charge_type, actual_hours):
        self.time_entries.append((charge_type, actual_hours))

    def add_time_sheet(self, time_sheet_id, hours, status, period):
        self.time_sheet = {
            "id": time_sheet_id,
            "hours": hours,
            "status": status,
            "period": period
        }
    
    def get_time_entries(self):
        return self.time_entries

    def get_time_sheet(self):
        return self.time_sheet

    def cross_check(self):
        pass
    

class WorkWeek:
    
    def __init__(self):
        self.charge_codes = get_charge_codes()
        self.all_users = get_users_id_name()
        self.employees_time = {}
        
        self.failed_time_sheets = []
        self.failed_time_entries = []
        #print(self.charge_codes)

        for user_name, user_id in self.all_users.items():
            self.employees_time[user_id] = EmployeeTimeRecord(user_name, user_id)

    def process_prev_period(self, time_sheets_, time_entries_):
       
        for entry in time_entries_:
            try:  
                
                charge_id = entry['workType']['name']
                hours = entry['actualHours']

                self.employees_time[entry['member']['id']].add_time_entry(charge_id, hours)
            except KeyError:
                #print(f"this one has no charge type: {entry['id']}")
                self.employees_time[entry['member']['id']].add_time_entry(1, hours)

        for sheet in time_sheets_:
            try:
                self.employees_time[self.all_users[sheet.employee]].add_time_sheet(
                    sheet.timesheetID, sheet.hours, sheet.status, sheet.period
                )
            except KeyError:
                self.failed_time_sheets.append(sheet)
                

    def display_processed_results(self):
        print(self.employees_time.keys())
        for employee in self.employees_time:
            print(self.employees_time[employee].employee_name)
            print(self.employees_time[employee].get_time_sheet())
            print(self.employees_time[employee].get_time_entries())

    def convert_to_quickbooks_format(self):
        quickbooks_obj = {}
        for employee in self.employees_time:
            pass



# recent_period = get_time_period(date.today()) - 1
    

# start = date.fromisoformat("2022-12-03")
# end = date.fromisoformat("2022-12-07")

# entries = get_time_entries(start, end)
# sheets = get_all_timesheets(recent_period)

# print(entries[0].keys())

# test = WorkWeek()
# test.process_prev_period(sheets, entries)
# test.display_processed_results()

# print(str(sheets[0]))


# print(entries[0]['chargeToId'])

    