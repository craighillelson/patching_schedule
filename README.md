# patching_schedule

Python 3.8 script to build a patching schedule. After prompting the user for a target date, the script distributes a list of computers to patch over the Saturdays between the day the script is run and the target date.

# Requirement

[dateutil](https://pypi.org/project/python-dateutil/)

# Instructions

1. Download build_sched.py
1. Save a csv named "computers.csv" to the same directory. Include the following headers: "client,workstation,build" and populate the csv with the corresponding data.
1. From a terminal window, type "python3 build_sched.py"
