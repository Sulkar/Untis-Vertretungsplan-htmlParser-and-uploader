# Untis-Vertretungsplan-htmlParser-and-uploader

Python program to merge, change and upload http://untis.de/ HTML export!

![Alt text](/untisparser.png?raw=true "Program Python")

## Usage

- click on "update Config" -> "vertretungsplan.conf" will open
- add server = ..., username = ..., password = ... -> example: [vertretungsplan-example.conf](/vertretungsplan-example.conf)
- Choose folder for teacher today, teacher tomorrow, student today and student tomorrow with "subst_001 - subst_n" data
- click the "start program" button -> example: [tempUntisData](/tempUntisData/)

-> the "subst_001 - subst_n" data in the folders come from the untis html export

## Function
The program gets all "subst_001 - subst_n" data in the specified folder and do the following:
- merge all files in the folder to one file i.e.: "LehrerAllHeute.html"
- change the html of the file to remove styles and some tags which aren´t needed -> see: [myHtmlParser.py](/classes/myHtmlParser.py)
- add some specific ID´s, which are needed for displaying the data correctly on the "https://github.com/Sulkar/Untis-Vertretungsplan-custom-website" website
