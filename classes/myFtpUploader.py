#
# myFtpUploader.py Class - to upload the generated html files to our webserver
#

import ftplib

# Class START
class myFtpUploader:

    tempFileName = ""

    def __init__(self, directory, _tempFileName):
        server = 'ftp.strato.com'
        username = 'ftp_vertretungsplan@mittelschule-unterschleissheim.de'
        password = 'vertretungsplan125'
        ftp_connection = ftplib.FTP(server, username, password)


        remote_path = directory
        ftp_connection.cwd(remote_path)
        #session = ftplib.FTP('example.com','username','password')
        file = open('E:/files/OneDrive/Programming/Python Programming/Untis-Vertretungsplan-htmlParser-and-uploader/tempUntisData/Lehrer heute/LehrerAllHeute.html', 'rb') # file to send
        ftp_connection.storbinary('STOR '+_tempFileName, file)     # send the file
        file.close()                                    # close file and FTP
        ftp_connection.quit()
