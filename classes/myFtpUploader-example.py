#
# myFtpUploader.py Class - to upload the generated html files to our webserver
#

import ftplib, os

# Class START
class myFtpUploader:

    server = ""
    username = ""
    password = ""

    def __init__(self):
        self.server = 'server'
        self.username = 'user'
        self.password = 'pass'


    def uploadHTML(self, _sourceDir, _finalDir, _tempFileName):
        ftp_connection = ftplib.FTP(self.server, self.username, self.password)
        ftp_connection.cwd(_finalDir)

        file = open(os.path.join(_sourceDir, _tempFileName), 'rb') # file to send
        ftp_connection.storbinary('STOR ' + _tempFileName, file)     # send the file
        file.close()                                    # close file and FTP
        ftp_connection.quit()
