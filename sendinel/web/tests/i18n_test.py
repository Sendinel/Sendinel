from django.core.urlresolvers import reverse
from django.test import TestCase


class InternationalizationTest(TestCase):
    fixtures = ['backend_test']
    urls = 'sendinel.urls'
    
    def setUp (self):
        # we're using Traditional Chinese as Test language
        data = {'language': 'zh-tw'}
        url = reverse("django.views.i18n.set_language")
        self.client.post(url, data)
    
    def test_jsi18n(self):
        response = self.client.get("/jsi18n/")
        self.failUnlessEqual(response.status_code, 200)
        # assert at least one translation is in the catalog
        self.assertContains(response, "catalog['")
        
    def test_i18n(self):
        response = self.client.get("/web/")
        self.assertContains(response, "#TRANSLATED#")

