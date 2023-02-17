from datetime import date
import get_time_sheets
from get_time_entries import get_time_entries
from employee_work_week import WorkWeek

time_periods = get_time_sheets.get_all_time_periods()
recent_period = get_time_sheets.get_time_period(date.today())

start_and_end = time_periods[recent_period]

# pulls the dates from the start and end of the most recent period 
start = date.fromisoformat(start_and_end['startDate'])
end = date.fromisoformat(start_and_end['endDate'])

time_sheets = get_time_sheets.get_all_timesheets(recent_period)
time_entries = get_time_entries(start, end)

work_week = WorkWeek()
work_week.process_prev_period(time_sheets, time_entries)
work_week.display_processed_results()


#print(str(time_sheets[0]))

