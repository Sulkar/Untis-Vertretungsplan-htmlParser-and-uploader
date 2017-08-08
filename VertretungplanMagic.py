#
# Vertretungsplan merger - htmlParser - ftpUploader
#

import shutil, glob, os, sys
from appJar import gui
from configobj import ConfigObj

# import my classes
from classes.myHtmlParser import myHtmlParser

# Variables
tempLehrerHeute = ""
tempLehrerMorgen = ""
tempSchuelerHeute = ""
tempSchuelerMorgen = ""
configFilename = "vertretungsplan.conf"
tempResult = ""


#
# defs / functions
#
# Functions: write and read Config
def writeConf(fieldNr, _tempDir):
    config = ConfigObj(configFilename)
    if fieldNr == 1:
        config['lehrerDirHeute'] = _tempDir
    elif fieldNr == 2:
        config['lehrerDirMorgen'] = _tempDir
    else:
        config['schuelerDir'] = _tempDir
    config.write()


def readConf():
    config = ConfigObj(configFilename)
    try:  # check if value lehrer exists
        value1 = config['lehrerDirHeute']
        app.setEntry("LehrerEnt", value1, callFunction=True)
        global tempLehrerHeute
        tempLehrerHeute = value1
    except:
        print("no Lehrer value found")
    try:  # check if value lehrer exists
        value2 = config['lehrerDirMorgen']
        app.setEntry("LehrerEnt2", value2, callFunction=True)
        global tempLehrerMorgen
        tempLehrerMorgen = value2
    except:
        print("no Lehrer value found")
    try:  # check if value schueler exists
        value3 = config['schuelerDirHeute']
        app.setEntry("SchuelerEnt", value3, callFunction=True)
    except:
        print("no Schüler value found")
    try:  # check if value schueler exists
        value4 = config['schuelerDirMorgen']
        app.setEntry("SchuelerEnt2", value4, callFunction=True)
    except:
        print("no Schüler value found")
# Function: merge files in current dataDir folder


def mergeFiles(dataDir, _tempFileName):
    if dataDir == "":
        print("Error no path available")
    else:
        # output Filename
        outfilename = os.path.join(dataDir, _tempFileName)

        # open all .htm files and merge them to the outfilename
        with open(outfilename, 'wb') as outfile:
            # for filename in glob.glob('*.htm'): -> list all files of current directory
            for filename in os.listdir(dataDir):
                if filename.endswith(".htm"):
                    tempFileName = os.path.join(
                        dataDir, filename)  # filename with dataDir
                    if tempFileName == outfilename:
                        # don't want to copy the output into the output
                        continue
                    with open(tempFileName, 'rb') as readfile:
                        shutil.copyfileobj(readfile, outfile)

# Function: app Buttons
def btn_LehrerHeute(btnName):
    _tempLehrerHeute = app.directoryBox(
        title="Lehrer Verzeichnis wählen:", dirName=None)
    app.setEntry("LehrerEnt", _tempLehrerHeute, callFunction=True)
    writeConf(1, _tempLehrerHeute)
def btn_LehrerMorgen(btnName):
    _tempLehrerMorgen = app.directoryBox(
        title="Lehrer Verzeichnis wählen:", dirName=None)
    app.setEntry("LehrerEnt2", _tempLehrerMorgen, callFunction=True)
    writeConf(2, _tempLehrerMorgen)

def btn_SchuelerHeute(btnName):
    _tempSchuelerHeute = app.directoryBox(
        title="Schüler Verzeichnis wählen:", dirName=None)
    app.setEntry("SchuelerEnt", _tempSchuelerHeute, callFunction=True)
    writeConf(3, _tempSchuelerHeute)
def btn_SchuelerMorgen(btnName):
    _tempSchuelerMorgen = app.directoryBox(
    title="Schüler Verzeichnis wählen:", dirName=None)
    app.setEntry("SchuelerEnt2", _tempSchuelerMorgen, callFunction=True)
    writeConf(4, _tempSchuelerMorgen)

# Function: start (merge, HTML parser, FTP uploader)
def btn_merge(btnName):
    global tempLehrerHeute, tempLehrerMorgen, tempResult
    tempResult = ""
    # merge files and clean html
    tempLehrerHeute = app.getEntry("LehrerEnt")
    tempLehrerMorgen = app.getEntry("LehrerEnt2")

    if tempLehrerHeute != "":
        mergeFiles(tempLehrerHeute, "LehrerAllHeute.html")
        tempResult += "-> Files merged in folder: " + tempLehrerHeute + "\n"
        tempParse = myHtmlParser(tempLehrerHeute, "LehrerAllHeute.html")
        tempResult += "-> HTML cleaned: " + tempParse.cleanHTML() + "\n"
    if tempLehrerMorgen != "":
        mergeFiles(tempLehrerMorgen, "LehrerAllMorgen.html")
        tempResult += "-> Files merged in folder: " + tempLehrerMorgen + "\n"
        tempParse = myHtmlParser(tempLehrerMorgen, "LehrerAllMorgen.html")
        tempResult += "-> HTML cleaned: " + tempParse.cleanHTML() + "\n"
    #log infos
    app.clearTextArea("resultMsg", callFunction=False)
    app.setTextArea("resultMsg", tempResult, callFunction=False)


#
# gui with appJar -> at the end of file to call def´s
#
app = gui("Vertretungsplan Form")
# app.setGeometry("400x300")
app.setResizable(canResize=False)

# add labels & entries in the correct row & column
app.addLabel("LehrerLab", "Verzeichnis Lehrer -> HEUTE:", 0, 0)
app.addEntry("LehrerEnt", 0, 1)
app.addNamedButton("ändern", "t_lehrer", btn_LehrerHeute, 0, 2)
app.addLabel("LehrerLab2", "Verzeichnis Lehrer -> MORGEN:", 1, 0)
app.addEntry("LehrerEnt2", 1, 1)
app.addNamedButton("ändern", "t_lehrer2", btn_LehrerMorgen, 1, 2)
app.addLabel("SchuelerLab", "Verzeichnis Schüler -> HEUTE:", 2, 0)
app.addEntry("SchuelerEnt", 2, 1)
app.addNamedButton("ändern", "t_schueler", btn_SchuelerHeute, 2, 2)
app.addLabel("SchuelerLab2", "Verzeichnis Schüler -> MORGEN:", 3, 0)
app.addEntry("SchuelerEnt2", 3, 1)
app.addNamedButton("ändern", "t_schueler2", btn_SchuelerMorgen, 3, 2)
app.addHorizontalSeparator(4,0,3, colour="red")
app.addNamedButton("MAGIC start!", "t_test", btn_merge, 5, 0, colspan=3)
app.addHorizontalSeparator(7,0,3, colour="red")
app.addLabel("messageLabel", "Result:", 8, 0, 3)
app.addScrolledTextArea("resultMsg", 9, 0, colspan=3)
#app.setTextAreaFg("resultMsg", "red")
app.setTextAreaBg("resultMsg", "LightYellow")

# read config file for input fields
readConf()

# start the GUI
app.go()
