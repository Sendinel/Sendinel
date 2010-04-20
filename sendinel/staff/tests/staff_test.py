from django.test import TestCase
from django.contrib.auth.models import User

class StaffTest(TestCase):
    def test_if_index_site_present_when_logged_in(self):
        # TODO refactor staff
        response = self.client.get("/staff/")
        self.assertTemplateUsed(response, 'staff/index.html')
        self.assertContains(response, 'Your are logged in')