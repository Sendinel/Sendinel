from random import random

from sendinel import settings

LINUX_AVAILABLE = False

try:
    import grp
    import os
    import pwd
    import shutil
    from subprocess import Popen, PIPE

    from hashlib import md5
    
    LINUX_AVAILABLE = True
    
except ImportError:
    print "Warning: Linux is required for voicecall functionality"
    
import time
import re

# TODO Test this!

class Voicecall:
    """
        This class takes responsibility for sending voicecalls and short messages
        through the asterisk telephony server
    """
    def __init__(self):
        self.asterisk_user = settings.ASTERISK_USER
        self.asterisk_group = settings.ASTERISK_GROUP
        self.asterisk_spool_dir = settings.ASTERISK_SPOOL_DIR  
        self.asterisk_extension = settings.ASTERISK_EXTENSION
        self.asterisk_sip_account = settings.ASTERISK_SIP_ACCOUNT
        self.asterisk_festivalcache = settings.FESTIVAL_CACHE
        self.asterisk_datacard = settings.ASTERISK_DATACARD 
        self.salutation = settings.CALL_SALUTATION

    def create_voicefile(self, text):
        """
            Create a soundfile for the given text, using a TTS engine
    
            @param  text:   the text to be read
            @type   text:   String
    
            @return The full file name of the sound file containing the text
        """

        text_hash = md5(text).hexdigest()
        filename = "%s/%s.ulaw" % (self.asterisk_festivalcache, text_hash)
        if not os.path.exists(filename):
            args = "-o %s -otype ulaw -" % (filename)
            
            if str(settings.LANGUAGE_CODE) == "en-us":
                pass
            elif str(settings.LANGUAGE_CODE) == "zu-za":
                args = args + ' -eval "(voice_csir_isizulu_buhle_multisyn)"'
                
             
            process = Popen(["text2wave"] + args.split(" "), stdin=PIPE)
            process.communicate(input=text)
        else:
            pass
        return "%s/%s" % (self.asterisk_festivalcache, text_hash)

    def create_spool_content(self, number, voicefile, salutation, extension,
                            sip_account, context):
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
        if(self.asterisk_datacard):
            output = """
Channel: Datacard/%s/%s
MaxRetries: 20
RetryTime: 20
WaitTime: 30
Context: %s
Extension: %s
Priority: 1
Set: PassedInfo=%s
Set: Salutation=%s
Archive: true
""" % (sip_account, number, context, extension, voicefile, salutation)
     
        else:
            output = """
Channel: SIP/%s@%s
MaxRetries: 20
RetryTime: 20
WaitTime: 30
Context: %s
Extension: %s
Priority: 1
Set: PassedInfo=%s
Set: Salutation=%s
Archive: true
""" % (number, sip_account, context, extension, voicefile, salutation)

        return output
       
    def create_sms_spool_content(self, text, number):
        """
            Create the asterisk spool file for a short message
            
            @param  text:   The text to be sent
            @type   text:   String
            
            @param  number:    The receipient's mobile phone number
            @type   number:    String
        """

        output = """
Channel: Local/2000
WaitTime: 2
RetryTime: 5
MaxRetries: 8000
Context: outbound-sms
Extension: s
Set: SmsNumber=%s
Set: Text=%s
Archive: true
""" % (number, text)

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
            uid = pwd.getpwnam(self.asterisk_user).pw_uid
            gid = grp.getgrnam(self.asterisk_group).gr_gid
            
            os.chown(filename, uid, gid)
            # set permissions to unix 666
            os.chmod(filename, 438)
            filename_new = str(time.time())
            filepath = self.asterisk_spool_dir + filename_new
            shutil.move(filename, filepath)
            return filename_new
            
        except:
            return False
           
    def replace_special_characters(self, text):
        """
           Replace all special characters in the passed string by '_'

           @param  text:      text to be freed from special characters
           @type   text:      String

           @return text without special characters
        """
        
        return re.sub('[^\x00-\x8f]', "_", text) 

    def conduct_sms(self, number, text, context):
        text = self.replace_special_characters(text)
        content = self.create_sms_spool_content(text, number)
        self.create_spool_file("tmp", content)
        return self.move_spool_file("tmp")

 
    def conduct_call(self, number, text, context): 
        """
            If Linux operating system is available, conduct a voice call
            
            @param  number:     Phone number to be called
            @type   number:     String
            
            @param  text:  text to be played when the call is conducted
            @type   text:  String
            
            @param  context:    Asterisk call context to be used for the outgoing call
            @type   context:    String
            
            @return True if spooling the call succeeded, if not False
        """
        
        if LINUX_AVAILABLE:
            text = self.replace_special_characters(text)
            salutation = self.create_voicefile(self.salutation)
            voicefile = self.create_voicefile(text)
            content = self.create_spool_content(number,
                                                voicefile,
                                                salutation,
                                                self.asterisk_extension,
                                                self.asterisk_sip_account,
                                                context)
            self.create_spool_file("tmp", content)
            return self.move_spool_file("tmp")
        else:
            return False
