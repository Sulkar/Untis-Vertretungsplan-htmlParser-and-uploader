#
# Vertretungsplan merger - htmlParser - ftpUploader
#

import shutil, os, sys, time, threading
from tkinter import *
from tkinter import filedialog, font
from tkinter.ttk import Separator
from configobj import ConfigObj

# import my classes
from classes.myHtmlParser import myHtmlParser
from classes.myFtpUploader import myFtpUploader

# Variables
tempLehrerHeute = ""
tempLehrerMorgen = ""
tempSchuelerHeute = ""
tempSchuelerMorgen = ""
configFilename = "vertretungsplan.conf"
tempResult = ""
thisResult = ""

#
# defs / functions
#
# Functions: write Config file
def writeConf(_fieldNr, _tempDir):
    print("write")
    config = ConfigObj(configFilename)
    if _fieldNr == 1:
        config['lehrerDirHeute'] = changeUmlauts(_tempDir, 1)
    elif _fieldNr == 2:
        config['lehrerDirMorgen'] = changeUmlauts(_tempDir, 1)
    elif _fieldNr == 3:
        config['schuelerDirHeute'] = changeUmlauts(_tempDir, 1)
    else:
        config['schuelerDirMorgen'] = changeUmlauts(_tempDir, 1)
    config.write()

# Functions: read Config file
def readConf():
    config = ConfigObj(configFilename)
    try:  # check if value lehrer exists
        value1 = config['lehrerDirHeute']
        value1 = changeUmlauts(value1, 2)
        e1.insert(0, value1)
        global tempLehrerHeute
        tempLehrerHeute = value1
    except:
        print("no Lehrer (heute) value found")
    try:  # check if value lehrer exists
        value2 = config['lehrerDirMorgen']
        value2 = changeUmlauts(value2, 2)
        e2.insert(0, value2)
        global tempLehrerMorgen
        tempLehrerMorgen = value2
    except:
        print("no Lehrer (morgen) value found")
    try:  # check if value schueler exists
        value3 = config['schuelerDirHeute']
        value3 = changeUmlauts(value3, 2)
        e3.insert(0, value3)
        global tempSchuelerHeute
        tempSchuelerHeute = value3
    except:
        print("no Schüler (heute) value found")
    try:  # check if value schueler exists
        value4 = config['schuelerDirMorgen']
        value4 = changeUmlauts(value4, 2)
        e4.insert(0, value4)
        global tempSchuelerMorgen
        tempSchuelerMorgen = value4
    except:
        print("no Schüler (morgen) value found")

# Function: merge files in current _dataDir folder
def mergeFiles(_dataDir, _tempFileName):
    if _dataDir == "":
        print("Error no path available")
    else:
        # output Filename
        outfilename = os.path.join(_dataDir, _tempFileName)
        # open all .htm files and merge them to the outfilename
        with open(outfilename, 'wb') as outfile:
            for filename in os.listdir(_dataDir):
                if filename.endswith(".htm"):
                    tempFileName = os.path.join(
                        _dataDir, filename)  # filename with _dataDir
                    if tempFileName == outfilename:
                        # don't want to copy the output into the output
                        continue
                    with open(tempFileName, 'rb') as readfile:
                        shutil.copyfileobj(readfile, outfile)

# Function: app Buttons
def btn_LehrerHeute():
    _tempLehrerHeute = filedialog.askdirectory()
    e1.delete(0, END)
    e1.insert(0, _tempLehrerHeute)
    writeConf(1, _tempLehrerHeute)
def btn_LehrerMorgen():
    _tempLehrerMorgen = filedialog.askdirectory()
    e2.delete(0, END)
    e2.insert(0, _tempLehrerMorgen)
    writeConf(2, _tempLehrerMorgen)
def btn_SchuelerHeute():
    _tempSchuelerHeute = filedialog.askdirectory()
    e3.delete(0, END)
    e3.insert(0, _tempSchuelerHeute)
    writeConf(3, _tempSchuelerHeute)
def btn_SchuelerMorgen():
    _tempSchuelerMorgen = filedialog.askdirectory()
    e4.delete(0, END)
    e4.insert(0, _tempSchuelerMorgen)
    writeConf(4, _tempSchuelerMorgen)

# Function: start (merge, HTML parser, FTP uploader)
def btn_start():
    global tempLehrerHeute, tempLehrerMorgen, tempSchuelerHeute, tempSchuelerMorgen, tempResult
    tempLehrerHeute = e1.get()
    tempLehrerMorgen = e2.get()
    tempSchuelerHeute = e3.get()
    tempSchuelerMorgen = e4.get()
    # clear output
    text1.delete(1.0, END)

    if tempLehrerHeute != "":
        # 1. merge all subst_00x files
        mergeFiles(tempLehrerHeute, "LehrerAllHeute.html")
        text1.insert(INSERT, "-> LehrerAllHeute.html merged!\n")
        root.update_idletasks() # updates the Tkinter form
        # 2. delete all not needed HTML
        tempParse1 = myHtmlParser()
        tempParse1.cleanHTML(tempLehrerHeute, "LehrerAllHeute.html")
        text1.insert(INSERT, "-> LehrerAllHeute.html parsed!\n")
        root.update_idletasks() # updates the Tkinter form
        # 3. upload the HTML file to the server in a new thread
        tempFtp1 = myFtpUploader()
        threadObj1 = threading.Thread(target=tempFtp1.uploadHTML, args=[tempLehrerHeute, "/data/Lehrer_heute/", "LehrerAllHeute.html"])
        threadObj1.start()
        threadObj2 = threading.Thread(target=checkThreads, args=[threadObj1, "-> LehrerAllHeute.html uploaded!\n"])
        threadObj2.start()
    if tempLehrerMorgen != "":
        mergeFiles(tempLehrerMorgen, "LehrerAllMorgen.html")
        text1.insert(INSERT, "-> LehrerAllMorgen.html merged!\n")
        root.update_idletasks() # updates the Tkinter form
        tempParse2 = myHtmlParser()
        tempParse2.cleanHTML(tempLehrerMorgen, "LehrerAllMorgen.html")
        text1.insert(INSERT, "-> LehrerAllMorgen.html parsed!\n")
        root.update_idletasks() # updates the Tkinter form
        tempFtp2 = myFtpUploader()
        # new threads for uploading and checking
        threadObj3 = threading.Thread(target=tempFtp2.uploadHTML, args=[tempLehrerMorgen, "/data/Lehrer_morgen/", "LehrerAllMorgen.html"])
        threadObj3.start()
        threadObj4 = threading.Thread(target=checkThreads, args=[threadObj3, "-> LehrerAllMorgen.html uploaded!\n"])
        threadObj4.start()

    if tempSchuelerHeute != "":
        mergeFiles(tempSchuelerHeute, "SchuelerAllHeute.html")
        text1.insert(INSERT, "-> SchuelerAllHeute.html merged!\n")
        tempParse3 = myHtmlParser()
        tempParse3.cleanHTML(tempSchuelerHeute, "SchuelerAllHeute.html")
        text1.insert(INSERT, "-> SchuelerAllHeute.html parsed!\n")
        tempFtp3 = myFtpUploader()
        # new threads for uploading and checking
        threadObj5 = threading.Thread(target=tempFtp3.uploadHTML, args=[tempSchuelerHeute, "/data/Schueler_heute/", "SchuelerAllHeute.html"])
        threadObj5.start()
        threadObj6 = threading.Thread(target=checkThreads, args=[threadObj5, "-> SchuelerAllHeute.html uploaded\n"])
        threadObj6.start()
    if tempSchuelerMorgen != "":
        mergeFiles(tempSchuelerMorgen, "SchuelerAllMorgen.html")
        text1.insert(INSERT, "-> SchuelerAllMorgen.html merged!\n")
        tempParse4 = myHtmlParser()
        tempParse4.cleanHTML(tempSchuelerMorgen, "SchuelerAllMorgen.html")
        text1.insert(INSERT, "-> SchuelerAllMorgen.html parsed!\n")
        tempFtp4 = myFtpUploader()
        # new threads for uploading and checking
        threadObj7 = threading.Thread(target=tempFtp4.uploadHTML, args=[tempSchuelerMorgen, "/data/Schueler_morgen/", "SchuelerAllMorgen.html"])
        threadObj7.start()
        threadObj8 = threading.Thread(target=checkThreads, args=[threadObj7, "-> SchuelerAllMorgen.html uploaded\n"])
        threadObj8.start()

# Function: replaces umlauts and vice versa -> ü=ue, ...
def changeUmlauts(_text, _type):
    if _type == 1:
        _text=_text.replace('ä', '/ae')
        _text=_text.replace('ö', '/oe')
        _text=_text.replace('ü', '/ue')
        return _text
    else:
        _text=_text.replace('/ae', 'ä')
        _text=_text.replace('/oe', 'ö')
        _text=_text.replace('/ue', 'ü')
        return _text

# Function: checks if thread is alive -> call Message when it´s dead
def checkThreads(thread, tempMessage):
    while thread.isAlive():
        #print("alive")
        pass
    else:
        text1.insert(INSERT, tempMessage, "RED")
        text1.see("end") # scroll to the end of text in textfield

#
# gui with appJar -> at the end of file
#

root = Tk()
root.wm_title("Untis Vertretungsplan Parser - Version 1.0")
root.resizable(False, False)
appHighlightFont = font.Font(family='Helvetica', size=12, weight='normal')
root.option_add("*Font", appHighlightFont)

# add labels & entries in the correct row & column
l1 = Label(root, text="Verzeichnis Lehrer -> HEUTE:")
l1.grid(row=0,column=0)
e1 = Entry(root)
e1.grid(row=0,column=1)
b1 = Button(root, text = "ändern", command = btn_LehrerHeute)
b1.grid(row=0,column=2)

l2 = Label(root, text="Verzeichnis Lehrer -> MORGEN:")
l2.grid(row=1,column=0)
e2 = Entry(root)
e2.grid(row=1,column=1)
b2 = Button(root, text = "ändern", command = btn_LehrerMorgen)
b2.grid(row=1,column=2)

l3 = Label(root, text="Verzeichnis Schüler -> HEUTE:")
l3.grid(row=2,column=0)
e3 = Entry(root)
e3.grid(row=2,column=1)
b3 = Button(root, text = "ändern", command = btn_SchuelerHeute)
b3.grid(row=2,column=2)

l4 = Label(root, text="Verzeichnis Schüler -> MORGEN:")
l4.grid(row=3,column=0)
e4 = Entry(root)
e4.grid(row=3,column=1)
b4 = Button(root, text = "ändern", command = btn_SchuelerMorgen)
b4.grid(row=3,column=2)

b5 = Button(root, text = "start parsing", command = btn_start)
b5.grid(row=4,column=0,columnspan=3)
sep1 = Separator(root, orient=HORIZONTAL)
sep1.grid(row=5,column=0,columnspan=3,sticky="ew")
l5 = Label(root, text="Result:")
l5.grid(row=6,column=0,columnspan=3)

text1 = Text(root, width=60, height=10)
text1.grid(row=7,column=0, columnspan=3)
text1.tag_config('RED', foreground='red')

l6 = Label(root, text="r.scheglmann@gmail.com")
l6.grid(row=8,column=0,columnspan=3)

# read config file for input fields
readConf()

# start the GUI
root.mainloop()
