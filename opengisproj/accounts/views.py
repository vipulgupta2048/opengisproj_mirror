# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.

def login(request):
    if request.user.is_authenticated == True:
        return redirect('/portal')
    return render(request, 'accounts/login.html')
