import re
from urllib.parse import urlparse
def log_reader():
    import re
    infosys_url = set()
    with open("ipslog.csv", "r", encoding='utf8') as file:
        for line in file:
            match = re.match(r'.*Download site:([^,]*),.*', line)
            if match != None and match.group(1) != " " and match.group(1).strip() != "null":
                infosys_url.add(match.group(1))
    return infosys_url