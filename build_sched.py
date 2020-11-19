"""Build a patching schedule for computers across clients."""

from datetime import date
from itertools import cycle
from collections import (namedtuple,
                         defaultdict)
import csv
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


def make_list_of_saturdays():
    i = 1
    lst = []
    for saturday in range(num_saturdays):
        saturday = sat_start + relativedelta(weekday=SA(+i))
        lst.append(saturday)
        i += 1
    return lst


def prompt_user_for_builds_to_exclude():
    lst = []
    while True:
        version = input("\nWhich version or versions would you like to "
                        "exclude? Enter nothing to exit.\n> ")
        if version == "":
            break
        lst = lst + [version]
    return lst


def open_csv_pop_dct_namedtuple():
    """
    Open a csv and populate, create a tuple from each row, and populate a
    list with the tuples created.
    """

    lst = []

    with open("computers.csv") as csv_file:
        f_csv = csv.reader(csv_file)
        headings = next(f_csv)
        assembled_tuple = namedtuple('assembled_tuple', headings)
        for detail in f_csv:
            row = assembled_tuple(*detail)
            lst.append((row.client, row.workstation, row.build))

    return lst


def exclude_builds_specified_user():
    """Populate a list of computers, skippiing the user specified builds."""

    lst = []
    for comp in clients_comps_builds:
        client = comp[0]
        name = comp[1]
        build = comp[2]
        if builds_to_exclude:
            if build in builds_to_exclude:
                pass
            else:
                lst.append([client, name])
        else:
            lst.append([client, name])

    return lst


def build_a_set_of_clients():
    lst = []
    for client in clients_comps:
        lst.append(client[0])

    return set(lst)


def make_dct():
    dct = defaultdict(list)
    for client, comp in clients_comps:
        dct[client].append(comp)
    return dct


def make_a_list_of_dictionaries():
    """
    Convert tuples to dictionaries. Populate a list with the resulting
    dictionaries.
    """

    lst = []
    for client, comp_name in dct_from_tuple.items():
        for account in clients:
            dct = {}
            if account == client:
                dct[client] = [comp_name]
                lst.append(dct)

    return lst


def build_sched():
    lst = []

    for dct in client_comps_list:
        for client, comp_details in dct.items():
            for comp, sat in zip(comp_details[0], cycle(saturdays)):
                lst.append((str(sat), client, comp))

    return lst


def make_ordered_sched():
    lst = []

    for date_client_comp in sorted(sched):
        lst.append(date_client_comp)

    return lst


def tuples_to_dictionary():
    dct = defaultdict(list)

    for sat, client, comp in ordererd_sched:
        dct[sat].append([client, comp])

    return dct


def output_schedule():
    print("\nsched dictionary")
    for sat, client_comp in schedule.items():
        print(sat)
        for details in client_comp:
            client = details[0]
            comp = details[1]
            print(client, comp)
        print("\n")


def write_dct_to_csv():
    """Write dictionary to csv."""

    with open("patching_schedule.csv", "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow(["patching schedule"])
        for sat, client_comps in schedule.items():
            out_csv.writerow([sat])
            keys_values = (client_comps)
            for details in client_comps:
                client = details[0]
                comp = details[1]
                keys_values = (client, comp)
                out_csv.writerow(keys_values)
            out_csv.writerow("")

    print('"patching_schedule.csv" exported successfully\n')


todays_date, target_date = prompt_user_for_target_date()
sat_start = find_saturday_following_date_specified(todays_date)
sat_end = find_saturday_following_date_specified(target_date)
num_saturdays = calc_num_weeks_between_dates(sat_end, sat_start)
saturdays = make_list_of_saturdays()
clients_comps_builds = open_csv_pop_dct_namedtuple()
builds_to_exclude = prompt_user_for_builds_to_exclude()
clients_comps = exclude_builds_specified_user()
clients = build_a_set_of_clients()
dct_from_tuple = make_dct()
client_comps_list = make_a_list_of_dictionaries()
sched = build_sched()
ordererd_sched = make_ordered_sched()
schedule = tuples_to_dictionary()
output_schedule()
write_dct_to_csv()
