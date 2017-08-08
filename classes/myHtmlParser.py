#
# myHtmlParser.py Class - to modify the html of the Untis Vertretungsplan HTML
#

import os, sys, re
from bs4 import BeautifulSoup

# Class START
class myHtmlParser:

    soup = ""
    tempFileName = ""

    def __init__(self, directory, _tempFileName):

        self.tempFileName = _tempFileName
        fileName = os.path.join(directory, _tempFileName)
        self.soup = BeautifulSoup(open(fileName), 'html.parser')

        # remove <html> tags, but let content untouched
        allHTML = self.soup.find_all("html")
        for v in allHTML:
            v.unwrap()

        # find all <head> and extract/remove it (head contains style and meta aswell)
        allHead = self.soup.find_all("head")
        for y in allHead:
            y.extract()

        # remove all table class=mon_head
        removeMonHead2nd = self.soup.find_all("table", class_="mon_head")
        for z in removeMonHead2nd:
            z.extract()

        # find footer (2 <p> after each day -> Braumandl and Untis Link)and remove it
        tempFooter = self.soup.find_all("table", class_="mon_list")
        for x in tempFooter:
            x.findNext("p").extract()
            x.findNext("p").extract()

        # find <body> tags and rename them to <div id="tempDay">
        tempBody = self.soup.find_all("body")
        for w in tempBody:
            w.name = "div"
            w["id"] = "tempDay"

        # save changed html to file
        # prettify("utf-8") or unicode(soup) for normal formatting
        #html_2 = self.soup.prettify("utf-8")
        html_2 = str(self.soup).encode("utf-8")
        with open(os.path.join(directory, _tempFileName), "wb") as file:
            file.write(html_2)

    def cleanHTML(self):
        return self.tempFileName
