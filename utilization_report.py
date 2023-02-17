from get_time_entries import get_time_entries
from get_charge_codes import get_charge_codes
from datetime import date
import json

smonth, sday, syear = input("Please enter the initial date, month day year   ex: 1 13 2023\n").split()
emonth, eday, eyear = input("Please enter the final date, month day year   ex: 1 20 2023\n").split()


start = date(int(syear), int(smonth), int(sday))
end = date(int(eyear), int(emonth), int(eday))

period_time = get_time_entries(start, end)
charge_codes = get_charge_codes()

check_file = open(f"UtilizationReport{str(start)}--{str(end)}-CHECKER.txt", "w")
check_file.write(f"Key value pair of CW charge codes --> {charge_codes}\n\n")

employee_totals = {} # "PTO- Bereavement (PAID)" "PTO-Vacation (PAID)" "PTO- Sick (Unpaid)" "Holiday"

for time in period_time:
    try:
        check_file.write(f"""\n{time['member']['name']}\nWork Type: {time['workType']['name']}\nCharge to ID: {time['chargeToId']}\nTime: {time['actualHours']}\nBillable: {time['billableOption']}\n""")
    except KeyError as err:
        if err == "chargeToId":
            check_file.write(f"""{time['member']['name']}\nWork Type: {time['workType']['name']}\nHours: {time['actualHours']}\nBillable: {time['billableOption']}\n""")

    if (time["member"]["name"] not in employee_totals 
        and (time['workRole']['name'] == "Engineer" or time['workRole']['name'] == "Technician")
    ):
        employee_totals[time['member']['name']] = {
            "total_hours_billed": 0,
            "total_hours_worked": 0
        }
        check_file.write(f"Added new employee to report: {time['member']['name']}\n")
    try:
        if (time['chargeToId'] == 4      # Holiday
            or time['chargeToId'] == 13  # PTO (Personal Time Off)- Vacation PAID
            or time['chargeToId'] == 20  # PTO- Sick (Unpaid)
            or time['chargeToId'] == 21  # PTO- Bereavement (PAID)
        ):  
            check_file.write(f"{time['member']['name']}: No Time added!1\n")
            continue
    except KeyError:
        pass

    try:
        if (time['workType']['name'] == "PTO- Bereavement (PAID)" 
            or time['workType']['name'] == "PTO-Vacation (PAID)"
            or time['workType']['name'] == "PTO- Sick (Unpaid)" 
            or time['workType']['name'] == "Holiday"
        ):
            check_file.write(f"{time['member']['name']}: No Time added!2\n")
            continue
    except KeyError:
        pass
        
        
    try:
        #Travel (In Town)  #Travel (Out of Town)  # 17 = Driving charge code
        if ((time['workType']['name'] == "Travel (In Town)" or time['workType']['name'] == "Travel (Out of Town)")
            or time['chargeToId'] == 17
        ):
            employee_totals[time['member']['name']]['total_hours_billed'] += time['actualHours']
            employee_totals[time['member']['name']]['total_hours_worked'] += time['actualHours']
            check_file.write(f"{time['member']['name']}: Drive time!!! billable baby!\n")
            continue
    except KeyError as err:
        if err == "chargeToId":
            if time['workType']['name'] == "Travel (In Town)" or time['workType']['name'] == "Travel (Out of Town)":
                employee_totals[time['member']['name']]['total_hours_billed'] += time['actualHours']
                employee_totals[time['member']['name']]['total_hours_worked'] += time['actualHours']
                check_file.write(f"{time['member']['name']}: Drive time!!! billable baby!\n")
                continue

    if (time['billableOption'] == "Billable"
        and time['workRole']['name'] == "Technician" or time['workRole']['name'] == "Engineer"
    ):
        employee_totals[time['member']['name']]['total_hours_billed'] += time["hoursBilled"]
        employee_totals[time['member']['name']]['total_hours_worked'] += time['actualHours']
        check_file.write("Adding billable time!!!\n")
    elif (time['billableOption'] != "Billable" 
        and time['workRole']['name'] == "Technician" or time['workRole']['name'] == "Engineer"
    ):
        employee_totals[time['member']['name']]['total_hours_worked'] += time['actualHours']
        check_file.write("Adding non-billable time\n")


result_sheet = open(f"UtilizationReport{str(start)}--{str(end)}.txt", "w")
result_sheet.write(f"Utilization report for {str(start)} --- {str(end)}\n\n")

for employee in employee_totals:
    try:
        billed_hours = employee_totals[employee]["total_hours_billed"]
        total_hours = employee_totals[employee]["total_hours_worked"]
        utilization = billed_hours / total_hours
        result_sheet.write(f"{employee} : {round(utilization, 2)}  --- Billed: {round(billed_hours, 2)} hrs , Total: {round(total_hours, 2)} hrs\n")
    except ZeroDivisionError:
        pass

