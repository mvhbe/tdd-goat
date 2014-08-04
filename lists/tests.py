#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import homePage


class HomePageTest(TestCase):

    def testRootUrlResolvesToHomePageView(self):
        """test root url resolves to home page"""
        found = resolve("/")
        self.assertEqual(found.func, homePage)

    def testHomePageReturnsCorrectHtml(self):
        """test home page returns correct html"""
        request = HttpRequest
        response = homePage(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
