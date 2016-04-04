# -*- coding: cp936 -*-
from django.db import models
# Create your models here.

class user(models.Model):
    username = models.CharField(max_length=30)
    userpassword = models.CharField(max_length=30)
    userqq = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name