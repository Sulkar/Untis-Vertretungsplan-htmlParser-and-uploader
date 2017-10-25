# Untis-Vertretungsplan-htmlParser-and-uploader

Python program to merge, modify and upload http://untis.de/ HTML export for your own needs! After uploading you can use the changed files to display them with a [custom substitution website](https://github.com/Sulkar/Untis-Vertretungsplan-custom-website)

![Alt text](/untisparser.png?raw=true "Program Python")

## Usage

- click on "update Config" -> "vertretungsplan.conf" will open
- add server = ..., username = ..., password = ... -> example: [vertretungsplan-example.conf](/vertretungsplan-example.conf)
- Choose folder for teacher today, teacher tomorrow, student today and student tomorrow with "subst_001 - subst_n" data -> example: [tempUntisData](/tempUntisData/)
- click the "start program" button

-> the "subst_001 - subst_n" data in the folders come from the untis html export

## Function
The program gets all "subst_001 - subst_n" data in the specified folder and do the following:
- merge all files in folder to one file i.e.: "LehrerAllHeute.html"
- change the html of the file to remove styles and some tags which aren´t needed -> see: [myHtmlParser.py](/classes/myHtmlParser.py)
- add some specific ID´s, which are needed for displaying the data correctly on the "https://github.com/Sulkar/Untis-Vertretungsplan-custom-website" website
- create a timeStamp.txt file with the current date and time
- upload all merged files and the timeStamp file to the specified ftp-server

## Dependencies
You need to pip install:
- "pip install configobj"
- "pip install beautifulsoup4"

## Build .exe with PyInstaller http://www.pyinstaller.org/
- (October 2017) PyInstaller works with Python 2.7 and 3.3—3.6
- use it in the directory of VertretungplanMagic.py with: "pyinstaller pyVertretungplanMagic.py"
- sometimes you need a shorter name to get PyInstaller to work -> i renamed VertretungsplanMagic.py to test.py
- all the data needed is in the "dist" folder
