#
# myFtpUploader.py Class - to upload the generated html files to our webserver
#

import ftplib

# Class START
class myFtpUploader:

    tempFileName = ""

    def __init__(self, finalDirectory, _tempFileName):
        server = 'server'
        username = 'username'
        password = 'password'
        ftp_connection = ftplib.FTP(server, username, password)


        remote_path = directory
        ftp_connection.cwd(remote_path)
        #session = ftplib.FTP('example.com','username','password')
        file = open('E:/files/OneDrive/Programming/Python Programming/Untis-Vertretungsplan-htmlParser-and-uploader/tempUntisData/Lehrer heute/LehrerAllHeute.html', 'rb') # file to send
        ftp_connection.storbinary('STOR '+_tempFileName, file)     # send the file
        file.close()                                    # close file and FTP
        ftp_connection.quit()
