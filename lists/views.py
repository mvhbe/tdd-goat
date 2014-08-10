#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item

def homePage(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect("/")

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

