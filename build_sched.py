"""Build a patching schedule for computers across clients."""

from collections import (namedtuple,
                         defaultdict)
from itertools import cycle
import csv
from datetime import date
import pyinputplus as pyip
from dateutil.relativedelta import relativedelta
from dateutil.rrule import SA


def prompt_user_for_target_date():
    """Prompt user for a date for target completion."""

    today = date.today()
    target = pyip.inputDate("\nPlease enter the target date for "
                            "completion (YYYY-MM-DD).\n> ",
                            formats=["%Y-%m-%d"])
    while True:
        if today > target:
            target = pyip.inputDate("\nPlease enter a date in the future."
                                    "\n> ", formats=["%Y-%m-%d"])
        else:
            break
    return today, target


def find_saturday_following_date_specified(sat):
    return sat + relativedelta(weekday=SA(+1))


def calc_num_weeks_between_dates(sat2, sat1):
    return int((sat2 - sat1).days / 7)


def create_list_of_saturdays():
    """
    Create a list of Saturdays equal to the number of Saturdays between the
    Saturday immediately following the start date and the Saturday immediately
    proceeding the target date for completion.
    """

    i = 1
    lst = []
    for saturday in range(num_saturdays):
        saturday = sat_start + relativedelta(weekday=SA(+i))
        lst.append(saturday)
        i += 1
    return lst


def prompt_user_for_builds_to_exclude():
    """Populate a list of builds to exclude."""

    lst = []
    while True:
        version = input("\nWhich version or versions would you like to "
                        "exclude? Enter nothing to exit.\n> ")
        if version == "":
            break
        lst = lst + [version]
    return lst


def open_csv():
    """
    Open csv and populate a list of tuples that excludes builds specified by the
    user.
    """

    lst = []

    with open("computers.csv") as csv_file:
        f_csv = csv.reader(csv_file)
        headings = next(f_csv)
        assembled_tuple = namedtuple('assembled_tuple', headings)
        for detail in f_csv:
            row = assembled_tuple(*detail)
            if row.build not in builds_to_exclude:
                lst.append((row.client, row.computer_name))

    return lst


def create_client_comps_dct():
    """
    Using defaultdict, make a dictionary structured as follows.
    key: client
    values: list of computer names
    """

    dct = defaultdict(list)
    for client_comps in comps:
        client = client_comps[0]
        comp_names = client_comps[1]
        dct[client].append(comp_names)

    return dct


def create_list_of_client_comps():
    """
    Make a list of dictionaries, with each dictionary structured as follows.
    key: client
    values: list of computers to update
    """

    lst = []
    for client, comps in client_comps.items():
        dct = {}
        dct[client] = comps
        lst.append(dct)
    return lst


def build_sched():
    """
    Loop through computer details and the list of Saturdays and assign
    computers to be updated to Saturdays.
    """

    dct1 = defaultdict(list)
    for dct2 in client_comps_dicts:
        for client, details in dct2.items():
            for client_comps, sat in zip(details, cycle(saturdays)):
                dct1[str(sat)].append([client, client_comps])
    return dct1


def output_schedule():
    """Output patching schedule to screen."""

    print("\npatching schedule")
    for sat, client_comp in schedule.items():
        for i in client_comp:
            client = i[0]
            comp_name = i[1]
            print(sat, client, comp_name)
        print("\n")


def write_to_csv(file_name):
    """Write patching schedule to csv."""

    with open(file_name, "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow(["saturday","client","computer_name"])
        for sat, client_comp_name in schedule.items():
            for i in client_comp_name:
                keys_values = (sat, *i)
                out_csv.writerow(keys_values)

    print(f'"{file_name}" exported successfully\n')


def find_average_computers_to_complete_weekly(lst1, lst2):
    avg_machines_per_week = int(len(lst1()) / len(lst2))
    print(f"You need to update an average of {avg_machines_per_week} per week "
          "to complete updates on time.")


todays_date, target_date = prompt_user_for_target_date()
sat_start = find_saturday_following_date_specified(todays_date)
sat_end = find_saturday_following_date_specified(target_date)
num_saturdays = calc_num_weeks_between_dates(sat_end, sat_start)
saturdays = create_list_of_saturdays()
builds_to_exclude = prompt_user_for_builds_to_exclude()
comps = open_csv()
client_comps = create_client_comps_dct()
client_comps_dicts = create_list_of_client_comps()
schedule = build_sched()
output_schedule()
write_to_csv("patching_schedule.csv")
find_average_computers_to_complete_weekly(open_csv, saturdays)
