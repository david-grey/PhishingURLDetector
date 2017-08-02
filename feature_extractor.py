import pandas as pd
import numpy as np
import csv
import urllib
import urllib.request
import requests
from xml.dom import minidom
from urllib.parse import urlparse
import re
import time
import asyncio


def google_api(url):
    try:
        data = """ 
        {
            "client": {
              "clientId":      "maliciousurl",
              "clientVersion": "1.0.1"
            },
            "threatInfo": {
              "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING"],
              "platformTypes":    ["WINDOWS"],
              "threatEntryTypes": ["URL"],
              "threatEntries": [
                {"url": "%s"},

              ]
            }
          }
          """ % url
        r = requests.post(
            'https://safebrowsing.googleapis.com/v4/threatMatches:find?key=AIzaSyCxRsIuA3GzMeUSsR0Xv4JO2mjjwSwJSkc',
            data, timeout=3.05)
        if r.json() != {}:
            r.close()
            return 1
        r.close()
        return 0
    except:
        return 0


def sitepopularity(host):
    xmlpath = 'http://data.alexa.com/data?cli=10&dat=snbamz&url=' + host
    # print xmlpath
    try:
        xml = urllib.request.urlopen(xmlpath).read()
        dom = minidom.parseString(xml)
        rank_host = find_ele_with_attribute(dom, 'REACH', 'RANK')
        # country=find_ele_with_attribute(dom,'REACH','RANK')
        rank_country = find_ele_with_attribute(dom, 'COUNTRY', 'RANK')
        if (rank):
            return 1
        else:
            return 0

    except:
        return 0


def Tokenise(url):
    if url == '':
        return [0, 0, 0]
    token_word = re.split('\W+', url)
    # print token_word
    no_ele = sum_len = largest = 0
    for ele in token_word:
        l = len(ele)
        sum_len += l
        if l > 0:  ## for empty element exclusion in average length
            no_ele += 1
        if largest < l:
            largest = l
    try:
        return [float(sum_len) / no_ele, no_ele, largest]
    except:
        return [0, no_ele, largest]


def extract_feature(row):
    url = row[0]
    label = row[1]
    if (label not in ['0', '1']):
        return {}

    feature = {}
    tokens_words = re.split('\W+', url)
    parsed_url = urlparse(url)
    if re.match(r'.*\d*\.\d*\.\d*\.\d*,*', str(parsed_url.netloc)) == None:
        feature["ip_consist"] = 0
    else:
        feature["ip_consist"] = 1
    # feature["length_of_url"] = len(url)
    feature["count_of_dot"] = url.count('.')
    feature["count_of_do"] = url.count('$')
    feature["length_of_domain"] = len(parsed_url.netloc)
    feature["count_of_@"] = url.count('@')
    feature["count_of_exe"] = url.count('exe')
    feature["count_of_redirect"] = url.count('//') - ("://" in url)
    feature["https"] = 0
    feature["count_of_hyphen"] = parsed_url.netloc.count('-')
    # feature["length_of_query"] = len(parsed_url.query.split('&')) if parsed_url.query else 0
    feature["not_port_80"] = 1 if (url.count(":") - ("://" in url)) > 0 else 0
    feature['avg_token_length'], feature['token_count'], feature['largest_token'] = Tokenise(url)
    feature['avg_domain_token_length'], feature['domain_token_count'], feature['largest_domain'] = Tokenise(
        parsed_url.netloc)
    feature['avg_path_token'], feature['path_token_count'], feature['largest_path'] = Tokenise(parsed_url.path)
    feature['rank_host'] = sitepopularity(parsed_url.netloc)
    feature['google'] = google_api(url)
    # feature['rank_host'],feature['rank_country'] =sitepopularity(parsed_url.netloc)
    '''
    if (feature["ip_consist"] == 0):
        feature["TLD"] = urlparse(url).netloc.split(".")[-1]
    else :
        feature["TLD"] = None
    '''
    feature["label"] = int(label)

    return feature

def predict_feature(url,feature):
    parsed_url = urlparse(url)
    if re.match(r'.*\d*\.\d*\.\d*\.\d*,*',str(parsed_url.netloc)) == None:
        feature["ip_consist"] = 0
    else:
        feature["ip_consist"] = 1
    #feature["length_of_url"] = len(url)
    tokens_words=re.split('\W+',url)
    feature["count_of_exe"] = url.count('exe')
    feature["length_of_domain"] = len(parsed_url.netloc)
    feature["count_of_@"] = url.count('@')
    feature["count_of_dot"] = url.count('.')
    feature["count_of_do"] = url.count('$')
    feature["count_of_redirect"] = url.count('//') - ("://" in url)
    feature["https"] = 0
    feature["count_of_hyphen"] = parsed_url.netloc.count('-')
    feature['avg_token_length'],feature['token_count'],feature['largest_token'] = Tokenise(url)
    feature['avg_domain_token_length'],feature['domain_token_count'],feature['largest_domain'] = Tokenise(parsed_url.netloc)
    feature['avg_path_token'],feature['path_token_count'],feature['largest_path'] = Tokenise(parsed_url.path)
    # feature["length_of_query"] = len(parsed_url.query.split('&')) if parsed_url.query else 0
    feature["not_port_80"] = 1 if (url.count(":") - ("://" in url))>0 else 0
    feature['rank_host'] = sitepopularity(parsed_url.netloc)
    feature['google'] = google_api(url)
    '''
    if (feature["ip_consist"] == 0):
        tld = "TLD_" + urlparse(url).netloc.split(".")[-1].strip()
        feature[tld] = 1
    for i in feature:
        if feature[i] == []:
            feature[i] = 0
    '''
    feature['url'] = url
    return feature

def main():
    start = time.time()
    ls = []
    loop = asyncio.get_event_loop()

    async def main():
        with open("data/datan.csv", "r", encoding='utf8') as data:
            csvfile = csv.reader(data)
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(
                    None,
                    extract_feature,
                    row
                )
                for row in csvfile
            ]
        for response in await asyncio.gather(*futures):
            ls.append(response)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    """
    pool = ThreadPoolExecutor(100)
    ls = []
    source = []
    cnt = 0
    with open("data.csv","r", encoding='utf8') as data:
        csvfile = csv.reader(data)
        for row in csvfile:
            cnt += 1
            source.append(row)
            ls.append(extract_feature(row))
            if cnt % 40 == 0:
                print (cnt)
            if cnt > 10:
                break

    while not q.empty():
        cnt -= 1
        if cnt % 40 == 0:
            print (cnt)
        ls.append(q.get().result())
    """

    print(time.time() - start)
    featureSet = pd.DataFrame(ls)
    featureSet = featureSet.fillna(0.0)
    featureSet.to_csv("data/train.csv")

if __name__ == '__main__':
    main()