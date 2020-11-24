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


def prompt_user_for_builds_to_exclude():
    lst = []
    while True:
        version = input("\nWhich version or versions would you like to "
                        "exclude? Enter nothing to exit.\n> ")
        if version == "":
            break
        lst = lst + [version]
    return lst


def open_csv(lst2):

    lst1 = []
    lst3 = []

    with open("computers.csv") as csv_file:
        f_csv = csv.reader(csv_file)
        headings = next(f_csv)
        assembled_tuple = namedtuple('assembled_tuple', headings)
        for detail in f_csv:
            row = assembled_tuple(*detail)
            lst1.append(row.client)
            dct = defaultdict(list)
            if row.build not in lst2:
                dct[row.client].append((row.computer_name, row.build))
                lst3.append(dct)

    return set(lst1), lst3


def find_saturday_following_date_specified(sat):
    return sat + relativedelta(weekday=SA(+1))


def calc_num_weeks_between_dates(sat2, sat1):
    return int((sat2 - sat1).days / 7)


def make_list_of_saturdays():
    i = 1
    lst = []
    for saturday in range(num_saturdays):
        saturday = sat_start + relativedelta(weekday=SA(+i))
        lst.append(saturday)
        i += 1
    return lst


def build_sched():
    lst = []
    for dct in computers:
        for client, details in dct.items():
            for detail in details:
                name = detail[0]
                lst.append((client, name))

    dct = defaultdict(list)
    for sat, client_comp in zip(cycle(saturdays), lst):
        dct[sat].append(client_comp)

    return dct


def output_schedule():
    for sat, comp in schedule.items():
        print(sat, comp)
    print("\n")


todays_date, target_date = prompt_user_for_target_date()
sat_start = find_saturday_following_date_specified(todays_date)
sat_end = find_saturday_following_date_specified(target_date)
num_saturdays = calc_num_weeks_between_dates(sat_end, sat_start)
saturdays = make_list_of_saturdays()
builds_to_exclude = prompt_user_for_builds_to_exclude()
clients, computers = open_csv(builds_to_exclude)
schedule = build_sched()
output_schedule()
