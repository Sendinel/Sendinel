from django.test import TestCase
from django.core.urlresolvers import reverse

from sendinel.settings import PROJECT_PATH
from sendinel.knowledgebase import views


class KnowledgeBaseTest(TestCase):

    def setUp(self):
        views.KNOWLEDGEBASE_DIRECTORY = PROJECT_PATH + "/knowledgebase/tests/content"
    
    def test_knowledge_base_on_main_page(self):  
        response = self.client.get(reverse('knowledgebase_index'))
        self.assertContains(response, "this_is_a_text.txt")
        self.assertContains(response, "this_is_a_picture.jpg")
        self.assertContains(response, "this_is_a_video.flv")

        

