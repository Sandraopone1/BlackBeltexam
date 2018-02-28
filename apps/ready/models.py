# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, post_data):

        errors = []
        
        if len(post_data["name"]) < 1:
            errors.append("name is required")
        elif len(post_data["name"]) < 2:
            errors.append("name must be at least 2 characters long")

        if len(post_data["alias"]) < 1:
            errors.append("alias is required")
        elif len(post_data["alias"]) < 2:
            errors.append("alias must be at least 2 characters long")

        if len(post_data["email"]) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(post_data["email"]):
            errors.append("Invalid email")
        else:
            list_of_users_matching_email = User.objects.filter(email=post_data["email"].lower())
            if len(list_of_users_matching_email) > 0:
                errors.append("Email already exists")

        if len(post_data["password"]) < 1:
            errors.append("Password is required")
        elif len(post_data["password"]) < 8:
            errors.append("Password must be 8 characters or more")

        if len(post_data["confirm"]) < 1:
            errors.append("Confirm password is required")
        elif post_data["password"] != post_data["confirm"]:
            errors.append("Confirm password must match Password")

        if len(post_data["date_of_birth"]) < 1:
            errors.append("Date of Birth is required")
        else:
            dob = datetime.strptime(post_data["date_of_birth"], "%Y-%m-%d")
            if dob > datetime.now():
                errors.append("Date of Birth must be in the past")

        if len(errors) > 0:
            return (False, errors)
        else:
            user = User.objects.create(
                name=post_data["name"], 
                alias=post_data["alias"], 
                email=post_data["email"].lower(), 
                password=bcrypt.hashpw(post_data["password"].encode(), bcrypt.gensalt()), 
                date_of_birth=dob
            )
            return (True, user)

    def login(self, post_data):
        
        response = {
            "errors": [],
            "is_valid": True,
            "user": None
        }

        if len(post_data["email"]) < 1:
            response["errors"].append("Email is required")
        elif not EMAIL_REGEX.match(post_data["email"]):
            response["errors"].append("Invalid email")
        else:
            list_of_users_matching_email = User.objects.filter(email=post_data["email"].lower())
            if len(list_of_users_matching_email) < 1:
                response["errors"].append("Email does not exist")

        if len(post_data["password"]) < 1:
            response["errors"].append("Password is required")
        elif len(post_data["password"]) < 8:
            response["errors"].append("Password must be 8 characters or more")

        if len(response["errors"]) < 1:
            user = list_of_users_matching_email[0]
            if bcrypt.checkpw(post_data["password"].encode(), user.password.encode()):
                response["user"] = user
            else:
                response["errors"].append("Password is incorrect")

        if len(response["errors"]) > 0:
            response["is_valid"] = False

        return response

class User(models.Model):
    name = models.CharField(max_length=255)
    alias= models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField()
    favorites = models.ManyToManyField("Quote", related_name="favorites", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    def __str__(self):
        return "name:{}, alias:{}, email:{}, password:{}, date_of_birth{}, created_at:{}, updated_at:{}".format(self.name, self.alias, self.email, self.password, self.date_of_birth, self.created_at, self.updated_at)
class QuoteManager(models.Manager):
    def validateQuote(self, post_data):

        is_valid = True
        errors = []

        if len(post_data.get('content')) < 12:
            is_valid = False
            errors.append('Message must be 12 characters and more')
        return (is_valid, errors)

class Quote(models.Model):
    content = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    poster = models.ForeignKey(User, related_name = 'authored_quotes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()

    def __str__(self):
        return 'content:{}, author:{}'.format(self.content, self.user)



