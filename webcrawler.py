#This is The Curious Rover. The Curious Rover can go anywhere in the internet.
#This is a test software should not be used in production. Unless necessary exception handling has been taken into account
'''Scrap urls from the internet. Process webpages and classify them according to topics of discussion.
Arrange them according to most visited sites and store the cluster(content related clusters). File processing and sharing.

Include interplanetary file transfer system protocols. Share links independently on the internet. 
Decentralized link transfer system.

Connect people to the free internet.
'''


from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random
from sys import setrecursionlimit

setrecursionlimit(100000)
pages=set()
random.seed(datetime.datetime.now())
#Retrieves a list of all internal links found on a page
def getInternalLinks(bs,includeUrl):
    includeUrl='{}://{}'.format(urlparse(includeUrl).scheme,urlparse(includeUrl).netloc)
    internallinks=[]
    #Find all links that begin with a '/'
    for links in bs.find_all('a',href=re.compile('^(/|.*'+includeUrl+')')):
        if links.attrs is not None:
            if links.attrs['href'] not in internallinks:
                if(links.attrs['href'].startswith('/')):
                    internallinks.append(includeUrl+links.attrs['href'])
                else:
                    internallinks.append(links.attrs['href'])
    return internallinks

#Retrieves a list of all external links found on the page
def getExternalLinks(bs,excludeUrl):
    externallinks=[]
    #Finds all links that start with 'http' that do not contain the current url
    for link in bs.find_all('a',href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externallinks:
                externallinks.append(link.attrs['href'])
    return externallinks

def getRandomExternalLink(startingPage):
    html=urlopen(startingPage)
    bs=BeautifulSoup(html,'html.parser')
    externalLinks=getExternalLinks(bs,urlparse(startingPage).netloc)
    if len(externalLinks)==0:
        print('No external link, looking around the site for one')
        domain='{}://{}'.format(urlparse(startingPage).scheme,urlparse(startingPage).netloc)
        internalLinks=getInternalLinks(bs,domain)
        return getRandomExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0,len(externalLinks)-1)]

def followExternalOnly(startingSite):
    print('Crawling the web')
    externalLink=getRandomExternalLink(startingSite)
    print('Random external link is {}'.format(externalLink))
    followExternalOnly(externalLink)

#Collecting a list of all external urls found in the site
allExtLinks=set()
allIntLinks=set()
def getAllExternalLinks(siteUrl):
    html=urlopen(siteUrl)
    domain='{}://{}'.format(urlparse(siteUrl).scheme,urlparse(siteUrl).netloc)
    bs=BeautifulSoup(html,'html.parser')
    internalLinks=getInternalLinks(bs,domain)
    externalLinks=getExternalLinks(bs,domain)

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)

    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            getAllExternalLinks(link)

allExtLinks.add('https://www.cointelegraph.com')
print(getAllExternalLinks('https://www.cointelegraph.com'))