"""This is a web scraper. The internet messanger bot. It scrapes the whole of the internet to obtain link data."""

import requests
from bs4 import BeautifulSoup

class Content:
    """Common base class for all articles/pages"""
    def __init__(self,url,title,body):
        self.url=url
        self.title=title
        self.body=body

    def print(self):
        """Flexible printing function controls output"""
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY:\n{}".format(self.body))

class Websites:
    """Contains information about website structure."""
    def __init__(self,name,url,titleTag,bodyTag):
        self.name=name
        self.url=url
        self.titleTag=titleTag
        self.bodyTag=bodyTag

class Crawler:
    def getPage(self,url):
        '''Downloading the html page of a website.'''
        try:
            req=requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text,'html.parser')
    
    def safeGet(self, pageObject, selector):
        """Utility function to get content string from a beautiful soup object and a selector. Returns empty string if no beautiful soup object was found for a given selector."""

        selectedElems=pageObject.select(selector)
        if selectedElems is not None and len(selectedElems)>0:
            return '\n'.join([elems.get_text() for elems in selectedElems])
        return " "

    def parse(self,site,url):
        """Extract content from a given page url"""
        bs=self.getPage(url)
        if bs is not None:
            title=self.safeGet(bs,site.titleTag)
            body=self.safeGet(bs,site.bodyTag)
            if title!=" " and body!=" ":
                content=Content(url,title,body)
                content.print()

crawler=Crawler()

siteData = [
['O\'Reilly Media', 'http://oreilly.com',
'h1', 'section#product-description'],
['Reuters', 'http://reuters.com', 'h1',
'div.StandardArticleBody_body_1gnLA'],
['Brookings', 'http://www.brookings.edu',
'h1', 'div.post-body'],
['New York Times', 'http://nytimes.com',
'h1', 'p.story-content']
]

websites = []

for row in siteData:
    websites.append(Websites(row[0], row[1], row[2], row[3]))

crawler.parse(websites[0], 'http://shop.oreilly.com/product/'\
'0636920028154.do')
crawler.parse(websites[1], 'http://www.reuters.com/article/'\
'us-usa-epa-pruitt-idUSKBN19W2D0')
crawler.parse(websites[2], 'https://www.brookings.edu/blog/'\
'techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/')
crawler.parse(websites[3], 'https://www.nytimes.com/2018/01/'\
'28/business/energy-environment/oil-boom.html')