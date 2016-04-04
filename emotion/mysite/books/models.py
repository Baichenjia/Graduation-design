# -*- coding: cp936 -*-
from django.db import models
# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    def __unicode__(self):
        return self.name

    #ָ��ģ�͵�ȱʡ����ʽ Publisher.objects.order_by("name")
    class Meta:
        ordering = ['name']

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    #����Author�����__unicode__()����������ͬʱ��ʾ���ߵ��պ���
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(null=True) # ��ʾ��������Ϊ��
    num_pages = models.IntegerField(blank=True,null=True)
    def __unicode__(self):
        return self.title

class user(models.Model):
    username = models.CharField(max_length=30)
    userpassword = models.CharField(max_length=30)
    userqq = models.CharField(max_length=30)
    def __unicode__(self):
        return self.username