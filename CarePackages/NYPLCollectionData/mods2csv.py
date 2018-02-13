import re
import requests
from lxml import etree as ET
import csv
import cStringIO
import codecs

#for utf8 encoding in csv output
class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()

def concatTitle(v):
    titlepart = ''
    nonsortpart = ''
    subtitlepart = ''
    partnumberpart = ''
    partnamepart = ''
    if v.find('./title') is not None:
        titlepart = v.find('./title').text.strip()
    if v.find('./nonSort') is not None:
        nonsortpart = v.find('./nonSort').text.strip() + ' '
    if v.find('./subTitle') is not None:
        subtitlepart = ': ' + v.find('./subTitle').text.strip()
    if v.find('./partNumber') is not None:
        partnumberpart = ', ' + v.find('./partNumber').text.strip()
    if v.find('./partName') is not None:
        partnamepart = ', ' + v.find('./partName').text.strip()
    fulltitle = nonsortpart + titlepart + subtitlepart + partnumberpart + partnamepart
    return fulltitle    

def getTitles(t, xpath):
    fulltitle = []
    values = t.xpath(xpath)
    for v in values:
        title = concatTitle(v)
        fulltitle.append(title)
    return fulltitle 

def getSubjectTitles(t, xpath):
    fulltitle = []
    values = t.xpath(xpath)
    for v in values:
        title = {}
        title['text'] = concatTitle(v)
        title['URI'] = v.get('valueURI')
        fulltitle.append(title)
    return fulltitle  

def getNames(t, xpath):
    values = t.findall(xpath)
    namevalues = []
    for v in values:
        name = {}
        name['contributorName'] = ' '.join([t.text for t in v.findall('./namePart')])
        name['contributorURI'] = v.get('valueURI')
        name['contributorType'] = v.get('type')
        if v.find('./role/roleTerm[@type="text"]') is not None:
            name['contributorRole'] = v.find('./role/roleTerm[@type="text"]').text
        else:
            name['contributorRole'] = None
        namevalues.append(name)
    if len(namevalues) == 0:
        namevalues = None
    return namevalues                              

def getSubjectNames(t, xpath):
    values = t.findall(xpath)
    namevalues = []
    for v in values:
        name = {}
        name['text'] = ' '.join([t.text for t in v.findall('./namePart')])
        name['URI'] = v.get('valueURI')
        namevalues.append(name)
    if len(namevalues) == 0:
        namevalues = None
    return namevalues     

def getDates(t, xpath):
    values = t.xpath(xpath)
    dates = {}
    dates['date'] = []
    rawencodeddates = []
    start = '' 
    end = ''
    for v in values:
        if v.xpath('@point="start"'):
            start = v.text
        elif v.xpath('@point="end"'):
            end = v.text
        else:
            dates['date'].append(v.text)
        if start != '' and end != '':
            #this assumes that you always have both 'start' and 'end' points and not just one or the other
            daterange = start + ' - ' + end
            dates['date'].append(daterange)
            start = ''
            end = ''
        if v.get('encoding'):
            rawencodeddates.append(v.text)
    if len(rawencodeddates) > 0:
        dates['dateStart'] = sorted(rawencodeddates)[0]
        dates['dateEnd'] = sorted(rawencodeddates)[-1]
    return dates   

def getSubjects(t, xpath):
    #still needs work on concatenation
    values = t.findall(xpath)
    texturivalues = []
    for v in values:
        subjecturi = {}
        subjecturi['text'] = ' -- '.join([t.text for t in v.xpath('.//*[text()]')])
        subjecturi['URI'] = v.get('valueURI')
        texturivalues.append(subjecturi)
    return texturivalues                                        

def getNotes(t, xpath):
    values = t.findall(xpath)
    notevalues = []
    for v in values:
        note = {}
        note['text'] = v.text
        if v.get('type') is not None:
            note['type'] = v.get('type')
        else:
            note['type'] = 'general'
        notevalues.append(note)
    return notevalues

def getValue(t, xpath):
    values = t.findall(xpath)
    textvalues = [v.text for v in values]
    if len(textvalues) == 0:
        textvalues = None
    return textvalues

def getValueAndUri(t, xpath):
    values = t.findall(xpath)
    texturivalues = []
    for v in values:
        texturi = {}
        texturi['text'] = v.text
        texturi['URI'] = v.get('valueURI')
        texturivalues.append(texturi)
    if len(texturivalues) == 0:
        texturivalues = None
    return texturivalues

def prepMods(mods):
    #remove xml declaration and any namespaces
    cleanmods = mods.replace('<?xml version="1.0" encoding="UTF-8"?>\n', '').replace('\n','')
    cleanmods = re.sub('<mods\s[^>]+">', '<mods>', mods, count=1)
    return cleanmods

def csvSetup(f):
    fieldnames = ['Source', 'Primary ID', 'Title', 'Alternative title', 'Contributor', 'Abstract', 'Date', 'Genre', 
              'Topical subject', 'Name subject' ,'Geographic subject', 'Title subject', 'Temporal subject',
              'Language', 'Type of resource', 'Place of publication', 'Publisher', 'Form', 'Extent', 'Notes', 'Link', 
              'Image']
    writer = DictUnicodeWriter(f, fieldnames=fieldnames)
    #writer = csvkit.unicsv.UnicodeCSVDictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    return writer

def modsToRow(item, source, writer):
    mods = prepMods(item['mods'])
    record = {}
    #get other stuff from record--imageid, link, thumbnails, etc.
    record['Source'] = source
    record['Link'] = item['link']
    record['Image'] = item['image']
    try:
        t = ET.fromstring(mods)
        record['Primary ID'] = item['primary_id']
        torpath = './typeOfResource'
        typeofresource = getValue(t, torpath)
        if typeofresource is not None:
            record['Type of resource'] = '|'.join(typeofresource)
        else:
            record['Type of resource'] = ''
        #preference language text over code
        langpath = 'language/languageTerm[@type="text"]'
        language = getValue(t, langpath)
        if language is not None:
            record['Language'] = '|'.join(language)
        else:
            langpath = 'language/languageTerm[@type="code"]'
            language = getValue(t, langpath)
            if language is not None:
                record['Language'] = '|'.join(language)
            else:
                record['Language'] = ''
        abspath = 'abstract'
        abstract = getValue(t, abspath)
        if abstract is not None:
            record['Abstract'] = '|'.join(abstract)
        else:
            record['Abstract'] = ''
        genrepath = './genre'
        genre = getValueAndUri(t, genrepath)
        if genre is not None:
            record['Genre'] = '|'.join([rr['text'] for rr in genre])
        else:
            record['Genre'] = ""
        topicpath = './subject/topic'
        topical = getValueAndUri(t, topicpath)
        if topical is not None:
            record['Topical subject'] = '|'.join(rr['text'] for rr in topical)
        else:
            record['Topical subject'] = '' 
        geopath = './subject/geographic'
        geographic = getValueAndUri(t, geopath)
        if geographic is not None:
            record['Geographic subject'] = '|'.join(rr['text'] for rr in geographic)
        else:
            record['Geographic subject'] = ''
        temppath = './subject/temporal'
        temporal = getValueAndUri(t, temppath)
        if temporal is not None:
            record['Temporal subject'] = '|'.join(rr['text'] for rr in temporal)
        else:
            record['Temporal subject'] = ''
        subjnamepath = './subject/name'
        subjectName = getSubjectNames(t, subjnamepath)
        if subjectName is not None:
            record['Name subject'] = '|'.join(rr['text'] for rr in subjectName)  
        else:
            record['Name subject'] = ''
        subjtitlepath = './subject/titleInfo'
        subjectTitle = getSubjectTitles(t, subjtitlepath)
        if subjectTitle is not None:
            record['Title subject'] = '|'.join(rr['text'] for rr in subjectTitle)
        else:
            record['Title subject'] = ''
        extentpath = './physicalDescription/extent'
        extent = getValue(t, extentpath)
        if extent is not None:
            record['Extent'] = '|'.join(extent)
        else:
            record['Extent'] = ''
        formpath = './physicalDescription/form'
        form = getValue(t, formpath)
        if form is not None:
            record['Form'] = '|'.join(form)
        else:
            record['Form'] = ''
        pubpath = './originInfo/publisher'
        publisher = getValue(t, pubpath)
        if publisher is not None:
            record['Publisher'] = '|'.join(publisher)
        else:
            record['Publisher'] = ''
        placepath = './originInfo/place/placeTerm'
        place = getValue(t, placepath)
        if place is not None:
            record['Place of publication'] = '|'.join(place)
        else:
            record['Place of publication'] = ''
        namepath = './name'
        contributor = getNames(t, namepath)
        if contributor is not None:
            record['Contributor'] = '|'.join([rr['contributorName'] for rr in contributor])
        else:
            record['Contributor'] = ''
        datepath = './originInfo/dateCreated | ./originInfo/dateIssued'
        dates = getDates(t, datepath)
        if len(dates['date']) > 0:
            record['Date'] = '|'.join(dates['date'])
        else:
            record['Date'] = ''
        notepath = './/note'
        notes = getNotes(t, notepath)
        if notes is not None:
            record['Notes'] = '|'.join((rr['type'] + ': ' + rr['text']) for rr in notes)
        else:
            record['Notes'] = ''
        titlepath = './titleInfo[@usage="primary"]'
        title = getTitles(t, titlepath)
        if len(title) > 0:
            record['Title'] = '|'.join(title)
            alttitlepath = './titleInfo[not(@usage)]'
            alttitle = getTitles(t, alttitlepath)
            if alttitle is not None:
                record['Alternative title'] = '|'.join(alttitle)
            else:
                record['Alternative title'] = ''
        else:
            #LoC doesn't use @usage attribute, so take the first instance of title as primary
            titlepath = './titleInfo'
            title = getTitles(t, titlepath)
            record['Title'] = title[0]
            alttitlepath = './titleInfo'
            alttitle = getTitles(t, alttitlepath)
            if len(alttitle) > 1:
                record['Alternative title'] = '|'.join(alttitle[1:])
            else:
                record['Alternative title'] = ''
    except:
        pass
    writer.writerow(record)
    return writer