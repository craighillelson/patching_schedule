"""
Open a csv and populate a list of dictionaries with the following structure.
key: client name
values: workstation name, build number
"""

from collections import defaultdict
from collections import namedtuple
import csv


def open_csv_pop_dct_namedtuple():
    """Open a csv and populate a dictionary."""

    lst = []

    with open("workstations.csv", "r") as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for r in f_csv:
            row = Row(*r)
            lst.append([row.client, row.workstation, row.build])

        return lst


clients_workstations = open_csv_pop_dct_namedtuple()
workstations_by_client = defaultdict(list)
for client, workstations, build in clients_workstations:
    workstations_by_client[client].append([workstations, build])

all_workstations = []
client_num_workstations = {}

for client, workstation_details in workstations_by_client.items():
    client_dct = {}
    client_dct[client] = workstation_details
    all_workstations.append(client_dct)
    client_num_workstations[client] = len(workstation_details)

print("\n")

for clients_workstations in all_workstations:
    print(clients_workstations)

print("\n")

for client, num_workstations in client_num_workstations.items():
    print(f"client: {client}")
    print(f"number of workstations: {num_workstations}\n")
