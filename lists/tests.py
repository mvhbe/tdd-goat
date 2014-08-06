#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
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
        expectedHtml = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expectedHtml)
