#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import homePage
from lists.models import Item

NEW_ITEM = 'A new list item'


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
        request.POST['item_text'] = NEW_ITEM

        response = homePage(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, NEW_ITEM)

    def testHomePageRedirectsAfterPost(self):
        """test home page redirects after post"""
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = NEW_ITEM

        response = homePage(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], "/lists/only-list")

    def testHomePageOnlySavesItemsWhenNecessary(self):
        """test home page only saves items when necessary"""
        request = HttpRequest()
        homePage(request)
        self.assertEqual(Item.objects.count(), 0)


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


class ListViewTest(TestCase):

    def testDisplaysAllItems(self):
        """listView displays all items"""
        Item.objects.create(text='Item 1')
        Item.objects.create(text='Item 2')

        response = self.client.get('/lists/only-list/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')

    def testUsesListTemplate(self):
        """listView uses template 'list.html'"""
        response = self.client.get('/lists/only-list/')
        self.assertTemplateUsed(response, 'list.html')

