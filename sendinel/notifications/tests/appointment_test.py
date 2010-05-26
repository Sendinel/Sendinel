from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from sendinel.backend.models import Hospital, \
                                    Patient, \
                                    ScheduledEvent, \
                                    get_woc
from sendinel.backend.tests.helper import disable_authentication
from sendinel.notifications.models import Notification, NotificationType
from sendinel.groups.forms import  NotificationValidationForm2, \
                                DateValidationForm


class NotificationViewTest(TestCase):
    fixtures = ['backend_test']
    urls = 'sendinel.urls'
    
    def setUp (self):
        self.hospital = Hospital.objects.get(current_hospital = True)
        self.client = Client()
        
    def test_notification_form_validation(self):
        data = {"phone_number" : "0123456789",
                "way_of_communication" : get_woc('sms').id}
        form = NotificationValidationForm2(data)
        self.assertTrue(form.is_valid())
        
        date = {"date" : "2010-08-12 12:00"}
        form_date = DateValidationForm(date)
        self.assertTrue(form_date.is_valid())

        
        data = { "phone_number" : "0123456rttddbh789",
                 "way_of_communication" : 3 }
        form = NotificationValidationForm2(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form['phone_number'].errors), 1)
        self.assertEquals(len(form['way_of_communication'].errors), 1)
        
        date = {"date" : "2010-08-45 12:00"}
        form_date = DateValidationForm(date)
        self.assertFalse(form_date.is_valid())         
        self.assertEquals(len(form_date['date'].errors), 1)   
    
    def create_notification_form(self, notification_type_id):
        notification_type = NotificationType.objects.get(
                                                    pk=notification_type_id)
        response = self.client.get(reverse('notifications_create', \
                kwargs={"notification_type_name": notification_type.name }))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="phone_number"')
        self.assertContains(response, 'name="way_of_communication"')
        return response

    
    
    def test_create_notification_form_notify_immediately(self):
        #labresult
        response = self.create_notification_form(3)
        self.assertNotContains(response, 'name="date"')
       
    
    def test_create_notification_form_dont_notify_immediately(self):
        #vaccination
        response = self.create_notification_form(1)
        self.assertContains(response, 'name="date"')

    
    
    def test_create_notification_submit_validations(self):
        notification_type = NotificationType.objects.get(pk=1) #vaccination
        response = self.client.post(reverse('notifications_create', \
            kwargs={"notification_type_name": notification_type.name }), 
                {'date': '2012-08-12',
                 'phone_number': '01733685224',
                 'way_of_communication': 1 })
        self.assertEquals(response.status_code, 302)
            
        response = self.client.post(reverse('notifications_create', \
                kwargs={"notification_type_name": notification_type.name }), 
                    {'date': '2012-08-12',
                     'phone_number': '01733assr685224',
                      'way_of_communication': '2' })
                      
        self.assertContains(response, 'Please enter numbers only')

        response = self.client.post(reverse('notifications_create', \
            kwargs={"notification_type_name": notification_type.name }), 
                {'date': '2012-08-12',
                    'phone_number': '685224',
                    'way_of_communication': 1  })
        self.assertContains(response, 'Please enter a cell phone number.')        

    def create_notification(self, way_of_communication):    
        notification_type = NotificationType.objects.get(pk=1) #vaccination
        self.client.get(reverse('notifications_create', \
                kwargs={"notification_type_name": notification_type.name }))
        
        data = {'date': '2012-08-12',
                'phone_number': '01733685224',
                'way_of_communication': str(way_of_communication.id)}
        return self.client.post(reverse('notifications_create',
                kwargs = {"notification_type_name": notification_type.name }),
                data)
        
    def create_and_save_notification(self, way_of_communication, phone_number):
        self.create_notification(way_of_communication)
        
        patient = Patient()
        patient.phone_number = phone_number
        self.client.post(reverse('web_authenticate_phonenumber'), \
                    {'patient': patient})
                    
        return self.client.get(reverse("notifications_save"))

    @disable_authentication
    def test_valid_create_notification(self):
        response = self.create_notification(get_woc('sms'))
        
        self.assertRedirects(response, reverse('notifications_save'))
        self.assertTrue(self.client.session.has_key('patient'))
        self.assertTrue(self.client.session.has_key('notification'))
        
    @disable_authentication
    def test_invalid_create_notification(self):
        response = self.create_notification(get_woc('voice'))
        
        self.failUnlessEqual(response.status_code, 200)        
        self.assertFalse(self.client.session.has_key('patient'))
        self.assertFalse(self.client.session.has_key('notification'))
        

    def save_notification_woc(self, way_of_communication):
        
        number_of_notifications = Notification.objects.count()
        number_of_events = ScheduledEvent.objects.count()
        
        phone_number = "01733685224"
        response = self.create_and_save_notification(way_of_communication, \
                                                    phone_number)
        
        self.failUnlessEqual(response.status_code, 200)
        
        appoint = Notification.objects.order_by("id").reverse()[:1][0]
        self.assertEquals(unicode(appoint.recipient.phone_number), phone_number)
        # test that exactly one Notification was created
        self.assertEquals(Notification.objects.count(),
                            number_of_notifications + 1)
        
        event = ScheduledEvent.objects.order_by("id").reverse()[:1][0]
        self.assertEquals(event.sendable, appoint)
        # test that exactly one ScheduledEvent was created
        self.assertEquals(ScheduledEvent.objects.count(),
                            number_of_events + 1)
        
    def test_create_notification_bluetooth(self):
        response = self.create_notification(get_woc('bluetooth'))
        self.assertRedirects(response, 
                             reverse('web_list_devices') + \
                             "?next=" + \
                             reverse('notifications_send'))
        self.assertTrue(self.client.session.has_key('patient'))
        self.assertTrue(self.client.session.has_key('notification'))
        
        response = self.client.get( reverse('notifications_send'), 
                { 'device_mac': '01733685224',
                 'date': '2012-08-12',
                 'way_of_communication': 1  })
        self.assertEquals(response.status_code, 200)
         
    def test_save_notification_sms(self):
         self.save_notification_woc(get_woc('sms'))

    def test_save_notification_voice(self):
        woc_voice = get_woc("voice")
        
        status_save = woc_voice.enabled
        
        woc_voice.enabled = True
        woc_voice.save()
    
        self.save_notification_woc(get_woc('voice'))
        
        woc_voice.enabled = status_save
        woc_voice.save()
         
    def test_create_notification_with_current_date(self):
        notification_type = NotificationType.objects.get(pk=3) #labresults
        response = self.client.post(reverse('notifications_create', \
            kwargs={"notification_type_name": notification_type.name }), 
                {'phone_number': '01733685224',
                 'way_of_communication': 1  })
        # validations test if date is correct. 
        # If not, there will be no 302 status code
        self.assertEquals(response.status_code, 302)
        
        
