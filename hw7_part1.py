import requests
import json
from bs4 import BeautifulSoup

header = {'User-Agent': 'SI_CLASS'}


CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url, header):
    unique_ident = get_unique_key(url)

    ## look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, headers=header)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]




#### Your Part 1 solution goes here ####

baseurl = 'https://www.si.umich.edu'
directory = '/directory?rid=All'
directory_html = make_request_using_cache(baseurl + directory, header=header)
d_soup = BeautifulSoup(directory_html, 'html.parser')


def get_umsi_data():
    #### Implement your function here ###
  titleslist = []
  nodeslist = []
  umsi_titles = {}
  content = d_soup.find('div', class_='view-content')

  emails = []

  nodes = content.find_all('a')
  for i in nodes:
    if "Contact Details" in str(i):
        nodeslist.append(i.get('href'))
  for i in nodeslist:
    profile = make_request_using_cache(baseurl + i, header=header)
    e_soup = BeautifulSoup(profile, 'html.parser')
    parse1 = e_soup.find(class_='field field-name-field-person-email field-type-email field-label-inline clearfix')
    parse2 = parse1.find('a')
    emails.append(parse2.text)

  names = content.find_all('div', property='dc:title')
  titles = content.find_all('div', class_="field field-name-field-person-titles field-type-text field-label-hidden")

  count = 0
  for k in titles:
    titleslist.append(k.text)
  for k in names:
    umsi_titles[k.text] = titleslist[count] + ' and ' + emails[count]
    count += 1

  dumps = json.dumps(umsi_titles)
  file = open('directory_dict.json', 'w')
  file.write(dumps)

  file.close()



#### Execute funciton, get_umsi_data, here ####

get_umsi_data()
#### Write out file here #####
