#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render


def homePage(request):
    return HttpResponse('<html><title>To-Do lists</title></html>')
