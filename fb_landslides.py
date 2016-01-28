
#! /usr/bin env python
import sys
import time

#This import is needed for Google search APIs
from apiclient.discovery import build

#for date time information
from datetime import date
import datetime, calendar, json
import os

#create  file every day for data collection
dt = datetime.datetime.now()
year = '%s' % (dt.year)
month = '%02d' % (dt.month)
day = '%02d' % (dt.day)
hour = '%02d' % (dt.hour)
minute = '%02d' % (dt.minute)


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def ensure_dir():
    directory = os.path.abspath("/aibek/facebook_landslide_"+year)
    if not os.path.exists(directory):
      os.makedirs(directory)
    dir_month =  os.path.abspath(directory+"/"+month)
    if not os.path.exists(dir_month):
      os.makedirs(dir_month)
    dir_day =  os.path.abspath(dir_month+"/"+day)
    if not os.path.exists(dir_day):
      os.makedirs(dir_day)
    dir_hour =  os.path.abspath(dir_day+"/"+hour)
    if not os.path.exists(dir_hour):
      os.makedirs(dir_hour)
    path = os.path.abspath( dir_hour + "/"+minute+'.json')
    if not os.path.exists(path):
      open(path, 'w').close()
    #check if path is created. comment later
    print path
    return path

#posts is used to retrieve json objects from the file
posts = []

#have a string with current date and time to be appended to the json object result being fetched from google
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def check(url):
    if not os.path.exists("links"):
        open("links", 'w').close()
        return
    datafile = file("links")
    #found = False #this isn't really necessary
    for line in datafile:
        if url in line:
           return True
    return False #because you finished the search without finding anything

#Method to get subsequent data from google
def queryNextIndex(service, index):
    #time.sleep(1)

#set up the query string
    res = service.cse().list(
        q='Landslides',
        cx='010608880857731338764:x3m0ywhradc',
        dateRestrict='d1',
#        orTerms='mudslides',
        siteSearch='www.facebook.com',
        siteSearchFilter='i',
        start=index,
    ).execute()

#fetch the correct page count and the pageIndex from which page we need to get the data

    for values in res['items']:
      if not check(values['link']):
        if not os.path.exists("links"):
          open("links", 'w').close()
        links_file = os.path.abspath("links")
        with open(links_file, 'a+') as links_f:
          links_f.write(values['link'] + '\n')

        path = ensure_dir()
        with open(path, 'a+') as f:
          values["time"] = now
          json.dump(values, f)
          f.write('\n')

#requests up to 10 results per page, for a maximum of 10 pages or 100 results. CSE limit
#We get HttpError 400 when requesting beyond 100 results and value returned is "Invalid value"

#Loop through to get all 10 pages
    #nextPageIndex = nextPageCount = 0
    if 'nextPage' in res['queries']:
        nextPageIndex = res['queries']['nextPage'][0]['startIndex']
        nextPageCount = res['queries']['nextPage'][0]['count']
        if nextPageCount != 0 and nextPageIndex < 101:
          queryNextIndex(service, nextPageIndex)


def main():

#specify the developerKey as given when registering
  service = build("customsearch", "v1",
             developerKey="your dev key")

# Make your first query.Set up the query fields
  res = service.cse().list(
  q='Landslides',
#  cx='011715665979575814697:bsl6l__jsma',
  cx='010608880857731338764:x3m0ywhradc',
  dateRestrict='d1',
#  orTerms='mudslides',
  siteSearch='www.facebook.com',
  siteSearchFilter='i',
  ).execute()

  for values in res['items']:
    if not check(values['link']):
      if not os.path.exists("links"):
        open("links", 'w').close()
      links_file = os.path.abspath("links")
      with open(links_file, 'a+') as links_f:
        links_f.write(values['link'] + '\n')
      path = ensure_dir()
      with open(path, 'a+') as f:
        values["time"] = now
        json.dump(values, f)
        f.write('\n')

  searchTerms = res['queries']['request'][0]['searchTerms']
  totalResults = res['queries']['request'][0]['totalResults']
  print("Search Query:" + searchTerms)
  print("Total Results:" + totalResults)
  if (totalResults > 10) and ('nextPage' in res['queries']):
    nextPageIndex = res['queries']['nextPage'][0]['startIndex']
    nextPageCount = res['queries']['nextPage'][0]['count']
    if nextPageCount != 0  and nextPageIndex < 101:
        queryNextIndex(service, nextPageIndex)


# Run code for mudslides as well
  res = service.cse().list(
  q='Landslides',
  cx='010608880857731338764:x3m0ywhradc',
 # cx='011715665979575814697:bsl6l__jsma',
  dateRestrict='d1',
  orTerms='mudslides',
  siteSearch='www.facebook.com',
  siteSearchFilter='i',
  ).execute()

  for values in res['items']:
    if not check(values['link']):
      if not os.path.exists("links"):
        open("links", 'w').close()
      links_file = os.path.abspath("links")
      with open(links_file, 'a+') as links_f:
        links_f.write(values['link'] + '\n')
      path = ensure_dir()
      with open(path, 'a+') as f:
        values["time"] = now
        json.dump(values, f)
        f.write('\n')

  link_file_length = file_len("links");
  if link_file_length > 1000:
    with open('links', 'r') as fin:
        contents = fin.read().splitlines(True)
    with open('links', 'w') as fout:
        fout.writelines(contents[1:])

if __name__ == '__main__':
  main()
