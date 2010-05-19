import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from sendinel.backend import bluetooth
from sendinel.backend.models import WayOfCommunication
from sendinel.notifications.models import AppointmentType

class BluetoothViewTest(TestCase):
    client = Client()
    
    fixtures = ["backend_test"]
    
    def test_get_bluetooth_devices(self):
        first_mac = "0011223344"
        first_value = "Hans Handy"
        second_mac = "9988776655"
        second_value = "Mobile Phone"
        valid_values = [first_value, second_value]
        valid_macs = [first_mac, second_mac]
    
        get_discovered_devices_old = bluetooth.get_discovered_devices
        
        def new_get_discovered_devices(Serveradress):
            #fake bluetooth device list with mac and name
            device_dict = {}
            device_dict[first_mac] = first_value
            device_dict[second_mac] = second_value
            return device_dict
        bluetooth.get_discovered_devices = new_get_discovered_devices
        
        response = self.client.post("/web/get_devices/")
        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(response["Content-Type"], "application/json")
        
        dict = json.loads(response.content)
        self.assertTrue(dict.has_key("devices"))
        array_devices = dict["devices"]
        
        self.assertEquals(len(array_devices), 2)
        self.assertTrue(array_devices[0].has_key("mac"))
        self.assertTrue(array_devices[0].has_key("name"))
        self.assertTrue(array_devices[0]["mac"] in valid_macs)
        self.assertTrue(array_devices[0]["name"] in valid_values)
        self.assertTrue(array_devices[1].has_key("mac"))
        self.assertTrue(array_devices[1].has_key("name"))
        self.assertTrue(array_devices[1]["mac"] in valid_macs)
        self.assertTrue(array_devices[1]["name"] in valid_values)
        
        bluetooth.get_discovered_devices = get_discovered_devices_old
        
    def test_send_appointment_via_bluetooth(self):   
        appointment_type = AppointmentType(name = "vaccination")
        appointment_type.save()
        
        appointment_type = AppointmentType.objects.get(pk=1)
        
        self.client.get(reverse('notifications_create', \
                kwargs={"appointment_type_name": appointment_type.name })) 
        data = {'date': '2012-02-22',
                'phone_number': '0175685444',
                'way_of_communication': "3"}
        self.client.post(reverse('notifications_create', \
                kwargs = {"appointment_type_name": appointment_type.name }), data)
        
        self.assertTrue(self.client.session.has_key("appointment"))
    
        old_send_vcal = bluetooth.send_vcal
             
        def return_true(val, val2, val3):
            return True
             
        bluetooth.send_vcal = return_true
        
        response = self.client.post(reverse("notifications_send"), {
                         "device_mac":"123456789"})
        
        self.assertEquals(response.status_code, 200)
        
        def return_false(val, val2, val3):
            return False
        
        bluetooth.send_vcal = return_false
        
        response = self.client.post(reverse("notifications_send"), {
                         "device_mac":"123456789"})
                         
        self.assertEquals(response.status_code, 500)
        
        bluetooth.send_vcal = old_send_vcal