#
# myFtpUploader.py Class - to upload the generated html files to our webserver
#

import ftplib

# Class START
class myFtpUploader:

    tempFileName = ""

    def __init__(self, sourceDir, finalDir, _tempFileName):
        server = 'server'
        username = 'username'
        password = 'password'
        ftp_connection = ftplib.FTP(server, username, password)

        ftp_connection.cwd(finalDir)
        file = open('E:/files/OneDrive/Programming/Python Programming/Untis-Vertretungsplan-htmlParser-and-uploader/tempUntisData/Lehrer heute/LehrerAllHeute.html', 'rb') # file to send
        ftp_connection.storbinary('STOR '+_tempFileName, file)     # send the file
        file.close()                                    # close file and FTP
        ftp_connection.quit()
