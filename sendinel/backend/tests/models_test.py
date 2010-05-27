from datetime import datetime

from django.test import TestCase

from django.db import IntegrityError

from sendinel import settings
from sendinel.backend.models import Hospital



class HospitalTest(TestCase):
    fixtures = ['backend_test']
    
    def test_get_hospital_no_hospital(self):
        Hospital.objects.all().delete()
        hospital = Hospital.get_current_hospital()
        self.assertTrue(1, Hospital.objects.all().count())
        self.assertEquals(Hospital.objects.all()[0].name, settings.DEFAULT_HOSPITAL_NAME)
        self.assertEquals(hospital.name, settings.DEFAULT_HOSPITAL_NAME)
    
    def test_get_hospital_with_hospital(self):
        hospital = Hospital.objects.get(current_hospital = True)
        self.assertEquals(Hospital.get_current_hospital(), hospital)


        
