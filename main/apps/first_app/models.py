# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be more than 2 characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be more than 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors["mail"] = "Email is not valid as it is not in the right format!"
        if not NAME_REGEX.match(postData['first_name']):
            errors["name_check_2"] = "First name should consist of alphabets only."
        if not NAME_REGEX.match(postData['last_name']):
            errors["name_check_3"] = "Last name should consist of alphabets only."
        if len(postData['date']) == 0:
            errors["date_check_1"] = "Date cannot be empty!"
        if postData['date'] > str(datetime.datetime.now()):
            errors["date_check_2"] = "Date is not valid!"
        if len(postData['password']) == 0:
            errors["password"] = "Password cannot be empty!"
        if len(postData['password']) > 8:
            errors["password"] = "Password cannot be more than 8 characters!"
        if postData['password'] != postData['con_password']:
            errors["password_check"] = "Password does not match confirm password!"
        if not len(errors):
            # all_users = User.objects.all()
            user = User.objects.filter(email = postData['email'])
            if user:
                errors["email_check"] = "This email already exists!"

        if not len(errors):
            pw = postData['password']
            hash_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            newUser = User.objects.create(first_name=postData['first_name'],last_name=postData['last_name'],email=postData['email'],password=hash_pw)
            errors["user"] = newUser

        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if user:
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors["password_check_2"] = "Password is incorrect!"
            else:
                errors["user"] = user[0]
        else:
            errors["email_check"] = "Login is not valid"

        return errors

class TemplateManager(models.Manager):
        def item_validator(self, request):
            errors = {}
            print "&&&&&", request.POST
            if len(request.POST['item']) == 0:
                errors["item"] = "Item cannot be empty!"
            if len(request.POST['item']) <3:
                errors["item"] = "Item name should be more than 3 characters long!"

            if not len(errors):
                item = Item.objects.filter(item = request.POST['item'])
                if item:
                    errors["item_check"] = "This item already exists! Please go back to dashboard to add to wishlist!"

            if not len(errors):
                user = User.objects.get(id = request.session['id'])
                newItem = Item.objects.create(item=request.POST['item'], createdby=user)
                newItem.wishedby.add(user)
                newItem.save()
                # errors["item"] = newItem

            return errors

# Create your models here.
class User(models.Model):
      first_name = models.CharField(max_length=255)
      last_name = models.CharField(max_length=255)
      email = models.EmailField(max_length=255,unique=True)
      datehired = models.DateField(auto_now_add = True)
      password = models.CharField(max_length=255)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = UserManager()

      # def __repr__(self):
      #     return 'User(first_name=%s, last_name=%s, email=%s, created_at=%s,updated_at=%s )'% (self.first_name, self.last_name, self.email, self.created_at, self.updated_at)
