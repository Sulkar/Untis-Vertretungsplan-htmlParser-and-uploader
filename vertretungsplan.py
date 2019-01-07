#
# Vertretungsplan merger - htmlParser - ftpUploader - Version 1.6
#

import shutil, os, sys, time
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
tempServer = ""
tempUsername = ""
tempPassword = ""
configFilename = "vertretungsplan.conf"
tempResult = ""
thisResult = ""
tempType = "" #ftp or local
localDir = "" #path to folder where to save the output


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
    global tempServer, tempUsername, tempPassword, tempLehrerHeute, tempLehrerMorgen, tempSchuelerHeute, tempSchuelerMorgen, tempType, localDir
    config = ConfigObj(configFilename)
    try: # check if type is specified
        tempType = config['type']
    except:
        print("no type specified")
    try: # check localDir is specified
        localDir = config['localDir']
    except:
        print("no localDir specified")
    try:  # check if value Servername exists
        tempServer = config['server']
        tempUsername = config['username']
        tempPassword = config['password']
    except:
        print("no FTP Server values found")

    try:  # check if value lehrer exists
        value1 = config['lehrerDirHeute']
        value1 = changeUmlauts(value1, 2)
        e1.delete(0, END)
        e1.insert(0, value1)
        tempLehrerHeute = value1
    except:
        print("no Lehrer (heute) value found")
    try:  # check if value lehrer exists
        value2 = config['lehrerDirMorgen']
        value2 = changeUmlauts(value2, 2)
        e2.delete(0, END)
        e2.insert(0, value2)
        tempLehrerMorgen = value2
    except:
        print("no Lehrer (morgen) value found")
    try:  # check if value schueler exists
        value3 = config['schuelerDirHeute']
        value3 = changeUmlauts(value3, 2)
        e3.delete(0, END)
        e3.insert(0, value3)
        tempSchuelerHeute = value3
    except:
        print("no Schüler (heute) value found")
    try:  # check if value schueler exists
        value4 = config['schuelerDirMorgen']
        value4 = changeUmlauts(value4, 2)
        e4.delete(0, END)
        e4.insert(0, value4)
        tempSchuelerMorgen = value4
    except:
        print("no Schüler (morgen) value found")

# Function: merge files in current _dataDir folder
def mergeFiles(_dataDir, _tempFileName, _outputDir):
    # store files creation date
    tempTime = 0
    # output Filename
    outfilename = os.path.join(_outputDir, _tempFileName)
    # open all .htm files and merge them to the outfilename
    with open(outfilename, 'wb') as outfile:
        for filename in os.listdir(_dataDir):
            if filename.endswith(".htm"):
                tempFileName = os.path.join(_dataDir, filename)  # filename with _dataDir
                if tempFileName == outfilename:
                    # don't want to copy the output into the output
                    continue
                # check creation time of the file (seconds) and merge only files created at the "same" time
                tempModifyTime = int(os.path.getmtime(tempFileName))
                tempCreateTime = int(os.path.getctime(tempFileName))
                if tempTime == 0:
                    tempTime = tempModifyTime
                    print("\n")
                    print("INIT  " + tempFileName + " - Modify Time: " + str(tempModifyTime) + " Creation Time: " + str(tempCreateTime))
                elif tempTime - 60 <=  tempModifyTime <= tempTime + 60: # if file has the same time or same time +- 60 seconds -> merge
                    print("MERGE " + tempFileName + " - Modify Time: " + str(tempModifyTime) + " Creation Time: " + str(tempCreateTime))
                else:
                    print("NO MERGE " + tempFileName + " - Modify Time: " + str(tempModifyTime) + " Creation Time: " + str(tempCreateTime))
                    continue

                with open(tempFileName, 'rb') as readfile:
                    shutil.copyfileobj(readfile, outfile)
    updateTextArea("-> " + _tempFileName + " merged!\n", "")

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
    # reread config -> if user changed it on runtime
    readConf()
    global tempLehrerHeute, tempLehrerMorgen, tempSchuelerHeute, tempSchuelerMorgen, tempResult
    tempLehrerHeute = e1.get()
    tempLehrerMorgen = e2.get()
    tempSchuelerHeute = e3.get()
    tempSchuelerMorgen = e4.get()
    # clear output
    text1.delete(1.0, END)

    if tempLehrerHeute != "":
        # create data folder for result
        outputDir = os.path.join(tempLehrerHeute, 'data')
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        #create Timestamp file
        createTimeStampFile()
        # 1. merge all subst_00x files
        mergeFiles(tempLehrerHeute, "LehrerAllHeute.html", outputDir)
        # 2. delete all not needed HTML and add new id´s
        tempParse1 = myHtmlParser()
        updateTextArea(tempParse1.cleanHTML(outputDir, "LehrerAllHeute.html"), "")
        # 3. upload the HTML file to the server in a new thread or copy files to network path
        if tempType == "ftp":
            tempFtp1 = myFtpUploader(tempServer, tempUsername, tempPassword)
            updateTextArea(tempFtp1.uploadHTML(outputDir, "/data/Lehrer_heute", "LehrerAllHeute.html"), "RED")
        elif tempType == "local":
            tempLocalDir = os.path.join(localDir, 'Lehrer_heute/')
            if not os.path.exists(tempLocalDir):
                os.makedirs(tempLocalDir)
            shutil.copy(os.path.join(outputDir, 'LehrerAllHeute.html'), tempLocalDir)


    if tempLehrerMorgen != "":
        outputDir = os.path.join(tempLehrerMorgen, 'data')
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        mergeFiles(tempLehrerMorgen, "LehrerAllMorgen.html", outputDir)
        tempParse2 = myHtmlParser()
        updateTextArea(tempParse2.cleanHTML(outputDir, "LehrerAllMorgen.html"), "")
        if tempType == "ftp":
            tempFtp2 = myFtpUploader(tempServer, tempUsername, tempPassword)
            updateTextArea(tempFtp2.uploadHTML(outputDir, "/data/Lehrer_morgen/", "LehrerAllMorgen.html"), "RED")
        elif tempType == "local":
            tempLocalDir = os.path.join(localDir, 'Lehrer_morgen/')
            if not os.path.exists(tempLocalDir):
                os.makedirs(tempLocalDir)
            shutil.copy(os.path.join(outputDir, 'LehrerAllMorgen.html'), tempLocalDir)

    if tempSchuelerHeute != "":
        outputDir = os.path.join(tempSchuelerHeute, 'data')
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        mergeFiles(tempSchuelerHeute, "SchuelerAllHeute.html", outputDir)
        tempParse3 = myHtmlParser()
        updateTextArea(tempParse3.cleanHTML(outputDir, "SchuelerAllHeute.html"), "")
        if tempType == "ftp":
            tempFtp3 = myFtpUploader(tempServer, tempUsername, tempPassword)
            updateTextArea(tempFtp3.uploadHTML(outputDir, "/data/Schueler_heute/", "SchuelerAllHeute.html"), "RED")
        elif tempType == "local":
            tempLocalDir = os.path.join(localDir, 'Schueler_heute/')
            if not os.path.exists(tempLocalDir):
                os.makedirs(tempLocalDir)
            shutil.copy(os.path.join(outputDir, 'SchuelerAllHeute.html'), tempLocalDir)

    if tempSchuelerMorgen != "":
        outputDir = os.path.join(tempSchuelerMorgen, 'data')
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        mergeFiles(tempSchuelerMorgen, "SchuelerAllMorgen.html", outputDir)
        tempParse4 = myHtmlParser()
        updateTextArea(tempParse4.cleanHTML(outputDir, "SchuelerAllMorgen.html"), "")
        if tempType == "ftp":
            tempFtp4 = myFtpUploader(tempServer, tempUsername, tempPassword)
            updateTextArea(tempFtp4.uploadHTML(outputDir, "/data/Schueler_morgen/", "SchuelerAllMorgen.html"), "RED")
        elif tempType == "local":
            tempLocalDir = os.path.join(localDir, 'Schueler_morgen/')
            if not os.path.exists(tempLocalDir):
                os.makedirs(tempLocalDir)
            shutil.copy(os.path.join(outputDir, 'SchuelerAllMorgen.html'), tempLocalDir)

    updateTextArea("-----------------------------------------------------------\n-> program finished!", "GREEN")

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

# Function: insert messages for text1 - Tkinter
def updateTextArea(tempMessage, tempColor):
    text1.insert(INSERT, tempMessage, tempColor)
    text1.see("end") # scroll to the end of text in textfield
    root.update_idletasks() # updates the Tkinter form

# Function: create and upload Timestamp text file
def createTimeStampFile():
    outputDir = os.path.join(tempLehrerHeute, 'data')
    file = open(os.path.join(outputDir, "timeStamp.txt"), "w")
    file.write(time.strftime("%d.%m.%Y um %H:%M"))
    file.close()
    if tempType == "ftp":
        tempFtp = myFtpUploader(tempServer, tempUsername, tempPassword)
        updateTextArea(tempFtp.uploadHTML(outputDir, "/data/", "timeStamp.txt"), "RED")
    elif tempType == "local":
        tempLocalDir = localDir
        if not os.path.exists(tempLocalDir):
            os.makedirs(tempLocalDir)
        shutil.copy(os.path.join(outputDir, 'timeStamp.txt'), tempLocalDir)


# Function: open config file with specified program (windows only?!?)
def openConfig():
    tempPath = os.path.join(os.path.dirname(__file__), "vertretungsplan.conf")
    os.system('"' + tempPath + '"')

#
# gui with appJar -> at the end of file
#
root = Tk()
root.wm_title("Untis Vertretungsplan Parser - Version 1.6")
root.resizable(False, False)

appHighlightFont = font.Font(family='Helvetica', size=12, weight='normal')
root.option_add("*Font", appHighlightFont)

# add menubar
menubar = Menu(root,bg="red")
menubar.add_cascade(label="update Config", command=openConfig)

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

b5 = Button(root, text = "start program", command = btn_start)
b5.grid(row=4,column=0,columnspan=3)
sep1 = Separator(root, orient=HORIZONTAL)
sep1.grid(row=5,column=0,columnspan=3,sticky="ew")
l5 = Label(root, text="Result:")
l5.grid(row=6,column=0,columnspan=3)

text1 = Text(root, width=60, height=10)
text1.grid(row=7,column=0, columnspan=3)
text1.tag_config('RED', foreground='red')
text1.tag_config('GREEN', foreground='green')

l6 = Label(root, text="r.scheglmann@gmail.com")
l6.grid(row=8,column=0,columnspan=3)

# read config file for input fields
readConf()

# start the GUI
root.config(menu=menubar)
root.mainloop()
