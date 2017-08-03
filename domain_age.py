
import whois
from dateutil import relativedelta


import datetime

def domain_age(domain):
    whois_info = whois.whois(domain.lower())

    if whois_info.creation_date:
        current_date = datetime.datetime.now()
        try:
            created_on = whois_info.creation_date[0]
            diff = relativedelta.relativedelta(current_date, created_on)
        except TypeError:
            return 0
    else:
        return 1
    return diff
