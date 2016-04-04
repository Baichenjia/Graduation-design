# -*- coding: cp936 -*-
__author__ = 'Bai Chenjia'

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def login_in(request):
    if request.method == 'POST':
        Username = request.POST.get("username")
        Password = request.POST.get("p")


    return render_to_response('login.html')