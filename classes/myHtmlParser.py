#
# myHtmlParser.py Class - to modify the html of the Untis Vertretungsplan HTML
#

import os, sys, re
from bs4 import BeautifulSoup

# Class START
class myHtmlParser:


    def __init__(self):
        pass

    def cleanHTML(self, _directory, _tempFileName):
        fileName = os.path.join(_directory, _tempFileName)
        soup = BeautifulSoup(open(fileName), 'html.parser')

        # remove <html> tags, but let content untouched
        allHTML = soup.find_all("html")
        for v in allHTML:
            v.unwrap()

        # find all <head> and extract/remove it (head contains style and meta aswell)
        allHead = soup.find_all("head")
        for y in allHead:
            y.extract()

        # remove all table class=mon_head
        removeMonHead2nd = soup.find_all("table", class_="mon_head")
        for z in removeMonHead2nd:
            z.extract()

        # find footer (2 <p> after each day -> Braumandl and Untis Link)and remove it
        tempFooter = soup.find_all("table", class_="mon_list")
        for x in tempFooter:
            x.findNext("p").extract()
            x.findNext("p").extract()

        # find <body> tags and rename them to <div id="tempDay">
        tempBody = soup.find_all("body")
        for w in tempBody:
            w.name = "div"
            w["id"] = "tempDay"

        # save changed html to file
        # prettify("utf-8") or unicode(soup) for normal formatting
        #html_2 = soup.prettify("utf-8")
        html_2 = str(soup).encode("utf-8")
        with open(os.path.join(_directory, _tempFileName), "wb") as file:
            file.write(html_2)

        return "-> " + _tempFileName + " parsed!\n"
