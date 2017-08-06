#
# myHtmlParser.py Class - to modify the html of the Vertretungsplan HTML
#

import os
import sys
import re
from bs4 import BeautifulSoup

# Class START


class myHtmlParser:

    soup = ""

    def __init__(self, directory, tempFileName):

        fileName = os.path.join(directory, tempFileName)
        self.soup = BeautifulSoup(open(fileName), 'html.parser')

        # save original html to prettified file
        # or unicode(soup) for normal formatting
        html_1 = self.soup.prettify("utf-8")
        with open(os.path.join(directory, "start_pretty.html"), "wb") as file:
            file.write(html_1)

        # find all <head> and extract/remove it (head contains style and meta aswell)
        allHead = self.soup.find_all("head")
        for y in allHead:
            y.extract()

        # remove all table class=mon_head -> after the first one
        removeMonHead2nd = self.soup.find_all("table", class_="mon_head")
        for z in removeMonHead2nd[1:]:  # starts with the second one!
            z.extract()

        # find footer (2 <p> after each day -> Braumandl and Untis Link)and remove it
        tempFooter = self.soup.find_all("table", class_="mon_list")
        for x in tempFooter:
            x.findNext("p").extract()
            x.findNext("p").extract()

        # save changed html to file
        # or unicode(soup) for normal formatting
        html_2 = self.soup.prettify("utf-8")
        with open(os.path.join(directory, "end_pretty.html"), "wb") as file:
            file.write(html_2)

    def getUpdate(self, sUpdate):
        tempS1 = self.soup.find("table", class_="mon_head")
        tempS2 = tempS1.tr.find_all("td")[2]
        tempStringU = tempS2.getText()  # get text out of element
        tempStringUArr = tempStringU.split()  # split string, word by word in array
        if sUpdate == "Day":
            return tempStringUArr[10]
        elif sUpdate == "Time":
            return tempStringUArr[11]

        # get current day
        #curDay1 = soup.find("div", class_="mon_title")
        #curDayArr = curDay1.getText().split()
        # curDayS1 = re.sub(r'#.*$', "", curDayArr[3])
        #curDayS2 = re.sub('\)', "", curDayArr[5])
        #print("aktueller Tag: " + curDayArr[1])
        #print("Seite " + curDayS1)
        #print("von " + curDayS2)
