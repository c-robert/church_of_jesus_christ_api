from church_of_jesus_christ_api import ChurchOfJesusChristAPI
from datetime import date
from sys import argv
import os

import logging
import contextlib
try:
    from http.client import HTTPConnection # py3
except ImportError:
    from httplib import HTTPConnection # py2

def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def debug_requests_off():
    '''Switches off logging of the requests module, might be some side-effects'''
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False

def find_member(list, surname, name):
    surname = surname.lower()
    names = {n.lower() for n in name.split()}
    member = None
    matches = 0
    for entry in list:
        if entry['nameFamilyPreferredLocal'].lower() == surname:
            entry_names = {n.lower() for n in entry['nameGivenPreferredLocal'].split()}
            x = names.intersection(entry_names)
            if len(x) > matches:
                member = entry
                matchs = len(x)
        elif member is not None:
            break
    return member


def load_attendance(file):
    list = []
    with open(file) as input:
        while True:
            line = input.readline()
            if not line:
                break
            else:
                name = line.strip().split()
                if len(name):
                    name.reverse()
                    list.append(tuple(name))
            

    list.sort()

    return list


if __name__ == '__main__':
    if len(argv) <= 1:
        print("Usage: attendance.py <input directory>")
    else:
        api = ChurchOfJesusChristAPI('robertd', 'bianchi2001bike')

        details = api.user_details

        unit = int(details["homeUnits"][0])

        members = api.get_member_list()

        files = os.listdir(argv[1])

        for file in files:
            if file.endswith('.txt'):
                # Get the attendance date
                attend_date = date.fromisoformat(os.path.splitext(file)[0])
                # Get the people that attended
                for person in load_attendance(os.path.join(argv[1], file)):
                    member = find_member(members, person[0], person[1])

                    if member is not None:
                        # Mark attended
                        print(api.update_attendance(member['uuid'], attend_date, True, unit))
                    else:
                        print(f"Unable to find: {person[0]}, {person[1]}")







