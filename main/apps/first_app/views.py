# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt

def index(request):
  return render(request,'first_app/index.html')

def registerUser(request):
    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)

        if 'user' in errors:
            request.session['first_name'] = errors['user'].first_name
            request.session['id'] = errors['user'].id
            request.session['route'] = "registered"
            return redirect('/success')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        return redirect('/')

def loginUser(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)

        if 'user' in errors:
            request.session['first_name'] = errors['user'].first_name
            request.session['id'] = errors['user'].id
            request.session['route'] = "logged in"
            return redirect('/success')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        return redirect('/')

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        return render(request,'first_app/success.html')

def logout(request):
    request.session.clear()
    return redirect('/')
