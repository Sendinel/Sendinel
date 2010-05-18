from django.test import TestCase

from sendinel.backend.models import WayOfCommunication, \
                                    get_enabled_wocs, \
                                    get_immediate_wocs, \
                                    get_woc


class WayOfCommunicationTest(TestCase):

    fixtures = ["backend_test"]

    def setUp(self):
        self.woc_sms = WayOfCommunication.objects.get(name = "sms")        
        self.woc_voice = WayOfCommunication.objects.get(name = "voice")
        self.woc_bluetooth = WayOfCommunication.objects.get(name = "bluetooth")

    def test_get_enabled_wocs(self):       
        enabled_wocs = get_enabled_wocs()
        
        self.assertTrue(self.woc_sms in enabled_wocs)
        self.assertTrue(not self.woc_voice in enabled_wocs)
        self.assertTrue(self.woc_bluetooth in enabled_wocs)
        
    def test_get_immediate_wocs(self):
        immediate_wocs = get_immediate_wocs()        
        
        self.assertTrue(self.woc_sms in immediate_wocs)
        self.assertTrue(not self.woc_voice in immediate_wocs)
        self.assertTrue(not self.woc_bluetooth in immediate_wocs)
        
    def test_get_woc(self):
        woc = get_woc("voice")
        
        self.assertEquals(woc.name, "voice")