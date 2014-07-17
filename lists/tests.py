from django.test import TestCase

class SmokeTest(TestCase):

    def testBadMaths(self):
        '''A smoke test'''
        self.assertEqual(1 + 1, 3)
