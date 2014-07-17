from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import homePage

class HomePageTest(TestCase):

    def testRootUrlResolvesToHomePageView(self):
        found = resolve("/")
        self.assertEqual(found.func, homePage)
