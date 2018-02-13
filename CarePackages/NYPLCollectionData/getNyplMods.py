#!/usr/bin/python

import requests
import configparser
from lxml import etree as ET
#import xml.etree.ElementTree as ET
import time
import mods2csv
import sys
import datetime
import json
import string
import os

#function to get captures for a given UUID
def getCaptures(uuid, titles='yes'):
    url = base + 'items/' + uuid + '?per_page=10000'
    if titles == 'yes':
        url = url + '&withTitles=yes'
    call = requests.get(url, headers={'Authorization': auth})
    return call.json()

#function to get the MODS XML for a given UUID
def getMODS(uuid, dataformat='.xml'):
    url = base + 'mods/' + uuid + dataformat
    call = requests.get(url, headers={'Authorization': auth})
    return call

def getCaptureDetails(uuid, dataformat='.xml'):
    url = base + 'items/item_details/' + uuid + dataformat
    call = requests.get(url, headers={'Authorization': auth})
    return call    

#function to get all MODS info and first capture thumbnails for items in an NYPL collection
def getItemsAndImages(uuid):
    response = getCaptures(uuid, titles='no')
    captures = response['nyplAPI']['response']['capture']
    items = []
    for c in captures:
        capturedetails = getCaptureDetails(c['uuid'])
        root = ET.fromstring(capturedetails.content)
        sibs = root.findall('./response/sibling_captures/capture')
        for s in sibs:
            if (c['uuid'] == s.find('./uuid').text) and (s.find('./orderInSequence').text == '1'):
                item = {}
                item['uuid'] = c['uuid']
                item['imageid'] = s.find('./imageID').text
                item['thumbnail'] = 'http://images.nypl.org/index.php?t=b&id=' + item['imageid']
                item['image'] = 'http://images.nypl.org/index.php?t=r&id=' + item['imageid']
                item['link'] = s.find('./itemLink').text
                item['mods'] = ET.tostring(root.find('./response/mods'))
                item['primary_id'] = root.findall('./response/mods/identifier[@type="uuid"]')[0].text
                items.append(item)
    return items

def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

#get collection data from API and create data package descriptor
def createDataPackage(uuid):
    response = getMODS(uuid).content
    xml = mods2csv.prepMods(response)
    root = ET.fromstring(xml)
    m = root.xpath('.//mods')[0]
    package = {}
    titlepath = './titleInfo[@usage="primary"]'
    title = mods2csv.getTitles(m, titlepath)
    if len(title) > 0:
        package['title'] = title[0]
    else:
        titlepath = './titleInfo'
        title = mods2csv.getTitles(m, titlepath)
        package['title'] = title[0]
    #convert title to package name by lowercasing, stripping non-ascii chars and extra whitespace, and replacing spaces with dash
    name = '-'.join(package['title'].translate(string.punctuation).lower().strip().split())
    package['name'] = removeNonAscii(name)
    package['profile'] = 'tabular-data-package'
    package['homepage'] = 'https://digitalcollections.nypl.org/collections/' + uuid
    package['created'] = datetime.datetime.now().isoformat()
    #default description text
    datanote = 'This dataset was created by harvesting the MODS XML records through the NYPL [Digital Collections API](http://api.repo.nypl.org) and crosswalking selected elements to a tabular format using Python scripts at https://github.com/saverkamp/beyond-open-data/CarePackages/NYPLCollectionsData'
    abspath = 'abstract'
    abstract = mods2csv.getValue(m, abspath)
    if abstract is not None:
        package['description'] = '|'.join(abstract)
        package['description'] = package['description'] + ' ' + datanote
    else:
        package['description'] = datanote
    #add the resource section for the csv
    resource = {}
    resource['path'] = '/' + package['name'] + '.csv'
    resource['name'] = package['name']
    resource['description'] = 'Metadata for digitized items from ' + package['title'] + ' in NYPL Digital Collections.'
    #use the schema json file for the data dictionary
    resource['schema'] = json.load(open('schema.json'))
    package['resources'] = []
    package['resources'].append(resource)
    return package
    
if __name__ == "__main__":
    #take uuid from first argument of command as collection uuid
    coll_uuid = sys.argv[1]
    #for testing
    #coll_uuid = 'ad7db6a0-c622-012f-80c3-58d385a7bc34'
    
    #create an instance of configparser, then read your config file into it
    config = configparser.ConfigParser()
    config.read('config.ini')
    #find your DC token in the config file content (by section and name) and assign it to a variable
    token = config.get('DC','token')
    #saving the base url in your config file will make it easier to find next time you want to use it
    base = config.get('DC', 'base')
    #now you're ready to put together your API calls
    auth = 'Token token=' + token
    
    #get the items and images for a given collection uuid and output a csv file
    coll = getItemsAndImages(coll_uuid)
    package = createDataPackage(coll_uuid)
    #create directory for data package
    newpath = package['name']
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    #create datapackage.json file
    packagepath = os.path.join(newpath, 'datapackage.json')
    with open(packagepath, 'w') as outfile:
        json.dump(package, outfile)
    #create output file and csvwriter
    filename = os.path.join(newpath, package['name'] + '.csv')
    f = open(filename, 'wb')
    writer = mods2csv.csvSetup(f)
    for c in coll:
        mods2csv.modsToRow(c, 'NYPL', writer)
    f.close()