from django.test import TestCase
from django.contrib.auth.models import User

class StaffTest(TestCase):
    def test_if_login_site_present(self):
        response = self.client.get("/staff/")
        self.assertRedirects(response, "/accounts/login/?next=/staff/")
        response = self.client.get("/staff/", follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')        
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'id_username')
        self.assertContains(response, 'id_password')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'name="next"')      
        
    def test_if_index_site_present_when_logged_in(self):
        user = User.objects.create_user('john', 'l@example.com', 'passwd')
        self.client.login(username='john', password="passwd")
        response = self.client.get("/staff/")
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Your are logged in')