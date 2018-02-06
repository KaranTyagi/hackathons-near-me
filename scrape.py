

# importing dependencies

import os
import time
import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------------
# Helper functions
#

# table is a list of lists
def print_table():
    global table
    print('\n  PID'.ljust(5) +'\tName'.ljust(18) +'\tStart'.ljust(10)+'\tEnd'.ljust(10)+'\tCity'.ljust(20)+'\tState'.ljust(12)+'\turl'.ljust(25)+'\tinfo'.ljust(55))

    for element in table:
        print('\n  {}'.format(element[0]).ljust(5) +'\t{}'.format(element[1]).ljust(18) +'\t{}'.format(element[2]).ljust(10)+ '\t{}'.format(element[3]).ljust(10) + '\t{}'.format(element[4]).ljust(20) +'\t{}'.format(element[5]).ljust(12)+'\t{}'.format(element[6]).ljust(25))
        #'\t{}'.format(element[07]).ljust(50))
    print('\n\tDone.')

def get_title(url):
    # might need delay otherwise flooding website with requests may block u.
    r = requests.get(url)
    p = r.content
    # create a beautifulsoup object
    soup = BeautifulSoup(html_doc)
    # get title
    return soup.title


def add_data():

    global table
    table = []  # [0] PID
                # [1] name
                # [2] start_date
                # [3] end_date
                # [4] city
                # [5] state
                # [6] URL    {website}
                # [7] info   {summary as extracted from title}

    id = 1
    mlh = requests.get('https://mlh.io/beta/events/')
    page = BeautifulSoup(mlh.text, 'html5lib')
    divs = page.findAll("div", {"class": "inner"})

    for d in divs:
        start_date = d.find("meta", {"itemprop": "startDate"})
        start_date = start_date.get('content')

        end_date = d.find("meta", {"itemprop": "endDate"})
        end_date = end_date.get('content')

        name = d.find('h3').get_text()

        website = d.findParent("a", {"class" : "event-link"}).get('href')

        #floodinf the website werver problem, so add manually
        # otherwise this script should run [on cloud or locally] once per day and update the info field in the table
        # how often to update the local/cloud database

        ''' info = get_title(website) '''

        city = d.find("span", {"itemprop" : "addressLocality"}).get_text()

        state = d.find("span", {"itemprop" : "addressRegion"}).get_text()

        # for location, distance etc module use :
        # us states dictionary in python
        # https://gist.github.com/rogerallen/1583593
        # https://gist.github.com/JeffPaine/3083347
        # https://stackoverflow.com/questions/40814187/map-us-state-name-to-two-letter-acronyms-that-was-given-in-dictionary-separately
        #https://pypi.python.org/pypi/us

        # pruning for 2018 events
        if int(str(end_date).split('-')[0]) < 2018:  # later replace by current date's year
            continue

        print(str(end_date).split('-')[0])
        # pruning hackathons before today

        table.append([id,name,start_date,end_date,city,state,website,'NA'])
        id+=1
        # end of for

if __name__ == "__main__":
    add_data()
    print_table()
