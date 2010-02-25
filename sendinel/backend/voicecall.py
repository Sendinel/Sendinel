import sendinel.settings

import grp
import os
import pwd
import shutil

import time

class Voicecall:
    def __init__(self):
        self.asterisk_user = settings.ASTERISK_USER
        self.asterisk_group = settings.ASTERISK_GROUP
        self.asterisk_spool_dir = settings.ASTERISK_SPOOL_DIR  

    def create_spool_content(self, number, voicefile, extension, sip_account, context):
        """
            Create the content for asterisk's spool file
            
            @param  number:         Phone number (may contain special chars)
            @type   number:         String
            
            @param  voicefile:      Name of the voice file which is supposed to be played when the call is conducted
            @type   voicefile:      String
            
            @param  extension:      Asterisk extension to be used for the call
            @type   number:         String

            @param  sip_account:    Asterisk SIP account to be used for the call
            @type   sip_account:    String
            
            @param  context:        Asterisk context for the outbound call
            @type   context:        String
            
            @return The text which can be put to a file, to make asterisk conduct the call
            """
            
        output = """
Channel: SIP/%s@%s
MaxRetries: 3
RetryTime: 20
WaitTime: 10
Context: %s
Extension: %s
Priority: 1
Set: PassedInfo=%s
""" %(number, sip_account, context, extension, voicefile)

        return output
        
    def create_spool_file(self, filename, content):
        """
            Create the asterisk spool file
            
            @param  filename:   File name for the temporary file
            @type   filename:   String
            
            @param  content:    Spool file content which is supposed to be written to the file
            @type   content:    String
        """
        
        test = open(filename, "w")
        test.write(content)
        test.close()

    
    def move_spool_file(self, filename):
        os.chown(filename, pwd.getpwnam(self.asterisk_user).pw_uid, grp.getgrnam(self.asterisk_group).gr_gid)
        filepath = self.asterisk_spool_dir + str(time.time)
        shutil.move(filename, filepath)