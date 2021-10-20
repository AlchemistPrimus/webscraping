from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError

def getTitle(url):
    '''This function gets the title of a website and returns None if title don't exist or returns the title.'''
    try:
        html=urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs=BeautifulSoup(html.read(),'html.parser')
        title=bs.body.h1
    except AttributeError as e:
        return None
    return title

title=getTitle("https://portal.jkuat.ac.ke/")
if title == None:
    print("Title could not be found")
else:
    print(title)
html=urlopen('https://portal.jkuat.ac.ke/')
bs=BeautifulSoup(html.read(),'html.parser')
print(bs)
