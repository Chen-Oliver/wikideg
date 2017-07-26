import requests,json,re
import page as pg

#regex to remove wiki namespaces(organizational pages)
#list of namespaces: https://en.wikipedia.org/w/api.php?action=query&meta=siteinfo&siprop=namespaces
regex = re.compile("(Media|Special|Talk|User|User talk|Wikipedia|Wikipedia talk|File|File talk|MediaWiki| \
MediaWiki talk|Template|Template talk|Help|Help talk|Category|Category talk|Portal|Portal talk|Book| \
Book talk|Draft|Draft talk|Education Program|Education Program talk|TimedText|TimedText talk|Module| \
Module talk|Gadget|Gadget talk|Gadget definition|Gadget definition talk)(?=:)")

#query for random page
randomQuery = "https://en.wikipedia.org/w/api.php?action=query&generator=random&grnnamespace=0&explaintext=true&prop=extracts|links&pllimit=500&exintro=1&exsentences=1&explaintext=true&format=json"

#search query in category
searchQuery = "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=%s+incategory:%s"

#used for dictionaries with arbitrary key
#input: dictionary
#return: value of next key in a dictionary
def getNextVal(d):
    return next(iter(d.values()),{"extract":"No page text found."})

#removes namespace links
#input: list of wiki links
#return list of non-namespace link titles
def remNamespace(links):
    filteredLinks=[]
    for link in links:
        if not regex.search(link["title"]):
            filteredLinks.append(link["title"])
    return filteredLinks

#returns JSON of query for random wikipedia page
def wikiJSON(query=randomQuery):
    response = requests.get(query)
    page = response.json()
    return page
#functions to access query data before storing in Page class
def getTitle(page):
    title = getNextVal(page["query"]["pages"])["title"]
    return title
def getLinks(page):
    links = getNextVal(page["query"]["pages"])["links"]
    return links
def getDescr(page):
    descr = getNextVal(page["query"]["pages"])["extract"]
    return descr

#search category for pageTitle, default category is disambiguation pages
def searchCategory(pageTitle,category="All_disambiguation_pages"):
    result = wikiJSON(searchQuery%(pageTitle,category))
    result= result["query"]["search"]
    if not result:
        return False
    else:
        return result[0]["title"] == pageTitle

#create start and end pages to store in Page class
def initPages():
    start = wikiJSON()
    end = wikiJSON()
    #start and end pages sohuld be different and shouldn't be disambiguation pages
    while(searchCategory(getTitle(start)) or searchCategory(getTitle(end)) and getTitle(start)==getTitle(end)):
        start = wikiJSON()
        end = wikiJSON()
    startPage = pg.Page(getTitle(start),getDescr(start),remNamespace(getLinks(start)))
    endPage = pg.Page(getTitle(end),getDescr(end),remNamespace(getLinks(end)))
    return (startPage,endPage)
