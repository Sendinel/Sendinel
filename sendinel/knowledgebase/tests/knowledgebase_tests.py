from django.test import TestCase
from django.core.urlresolvers import reverse

from sendinel.settings import PROJECT_PATH
from sendinel.knowledgebase import views

class KnowledgeBaseTest(TestCase):

    def setUp(self):
        views.KNOWLEDGEBASE_DIRECTORY = PROJECT_PATH + "/knowledgebase/tests/content"
    
    def test_knowledgebase_index(self):  
        response = self.client.get(reverse('knowledgebase_index'))
        self.assertContains(response, "this_is_a_text.txt")
        self.assertContains(response, "this_is_a_picture.jpg")
        self.assertContains(response, "this_is_a_video.flv")
        self.assertNotContains(response, ".file_with_dot")
        self.assertTrue(self.client.session.has_key('numbered_files'))

    def test_knowledgebase_show_jpg(self):
        response = self.client.get(reverse('knowledgebase_index'))
        files = self.client.session['numbered_files']
        file_id = get_key(files, 'this_is_a_picture.jpg')
        
        response = self.client.get(reverse('knowledgebase_show',
                                   kwargs={'file_id':file_id}))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "knowledgebase/show_jpg.html")
        self.assertContains(response, "<img src=")
        
    def test_knowledgebase_show_txt(self):
        response = self.client.get(reverse('knowledgebase_index'))
        files = self.client.session['numbered_files']
        file_id = get_key(files, 'this_is_a_text.txt')
    
        response = self.client.get(reverse('knowledgebase_show',
                                   kwargs={'file_id':file_id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "knowledgebase/show_txt.html")
        self.assertContains(response, "This is a text")

    def test_knowledgebase_show_video(self):
        response = self.client.get(reverse('knowledgebase_index'))
        files = self.client.session['numbered_files']
        file_id = get_key(files, 'this_is_a_video.flv')
        
        response = self.client.get(reverse('knowledgebase_show',
                                   kwargs={'file_id':file_id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "knowledgebase/show_video.html")
        
        
def get_key(dic, value_string):
        for key, value in dic.iteritems():
            if value == value_string: return key
