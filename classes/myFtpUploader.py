#
# myFtpUploader.py Class - to upload the generated html files to our webserver
#

import ftplib, os

# Class START
class myFtpUploader:

    server = ""
    username = ""
    password = ""

    def __init__(self, _server, _username, _password):
        self.server = _server
        self.username = _username
        self.password = _password


    def uploadHTML(self, _sourceDir, _finalDir, _tempFileName):
        try:
            ftp_connection = ftplib.FTP(self.server, self.username, self.password)
            ftp_connection.cwd(_finalDir)

            file = open(os.path.join(_sourceDir, _tempFileName), 'rb') # file to send
            ftp_connection.storbinary('STOR ' + _tempFileName, file)     # send the file
            file.close()                                    # close file and FTP
            ftp_connection.quit()
            return "-> " + _tempFileName + " uploaded!\n"
        except Exception as e:
            return "Error uploading " + _tempFileName + " !!! \n -> " + str(e) + "\n"
