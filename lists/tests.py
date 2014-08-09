#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import homePage
from lists.models import Item


class HomePageTest(TestCase):

    def testRootUrlResolvesToHomePageView(self):
        """test root url resolves to home page"""
        found = resolve("/")
        self.assertEqual(found.func, homePage)

    def testHomePageReturnsCorrectHtml(self):
        """test home page returns correct html"""
        request = HttpRequest()
        response = homePage(request)
        expectedHtml = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expectedHtml)

    def testHomePageCanSaveAPostRequest(self):
        """test home page can save a post request"""
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = homePage(request)

        self.assertIn('A new list item', response.content.decode())
        expectedHtml = render_to_string('home.html',
                                        {'new_item_text': 'A new list item'})
        self.assertEqual(response.content.decode(), expectedHtml)

class ItemModelTest(TestCase):

    def testSavingAndRetrievingItems(self):
        """test saving and retrieving items"""
        firstItem = Item()
        firstItem.text = "The first (ever) list item"
        firstItem.save()

        secondItem = Item()
        secondItem.text = "Item the second"
        secondItem.save()

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2)

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]
        self.assertEqual(firstSavedItem.text, firstItem.text)
        self.assertEqual(secondSavedItem.text, secondItem.text)
