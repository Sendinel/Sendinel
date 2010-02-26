import sendinel.settings

linux_available = False

try:
    import grp
    import os
    import pwd
    import shutil
    
    linux_available = True
    
except ImportError:
    print "Warning: Linux operating system is required to run the voicecall functionality"
    
import time

class Voicecall:
    def __init__(self):
        self.asterisk_user = sendinel.settings.ASTERISK_USER
        self.asterisk_group = sendinel.settings.ASTERISK_GROUP
        self.asterisk_spool_dir = sendinel.settings.ASTERISK_SPOOL_DIR  
        self.asterisk_extension = sendinel.settings.ASTERISK_EXTENSION
        self.asterisk_sip_account = sendinel.settings.ASTERISK_SIP_ACCOUNT

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
        """
            Rename the spool file and move it to the asterisk call spool directory
            
            @param  filename:   File name of the temporary file
            @type   filename:   String
            
            @return True if the operating succeeded, if not False
        """
        try:
            os.chown(filename, pwd.getpwnam(self.asterisk_user).pw_uid, grp.getgrnam(self.asterisk_group).gr_gid)
            filepath = self.asterisk_spool_dir + str(time.time)
            shutil.move(filename, filepath)
            return True
            
        except:
            return False
            
    def conduct_call(self, number, voicefile, context): 
        """
            If Linux operating system is available, conduct a voice call
            
            @param  number:     Phone number to be called
            @type   number:     String
            
            @param  voicefile:  name of the sound file to play when the call is conducted
            @type   voicefile:  String
            
            @param  context:    Asterisk call context to be used for the outgoing call
            @type   context:    String
            
            @return True if spooling the call succeeded, if not False
        """
        
        if linux_available:
            content = self.create_spool_content(number, voicefile, self.asterisk_extension, self.asterisk_sip_account, context)
            self.create_spool_file("tmp", content)
            return self.move_spool_file("tmp")
        else:
            return False
            