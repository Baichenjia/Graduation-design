# -*- coding: cp936 -*-
__author__ = 'Bai Chenjia'

from django.contrib import admin
from mysite.books.models import Publisher, Author, Book

#AuthorAdmin��django.contrib.admin.ModelAdmin�������������࣬������һ������Զ������ã��Թ�������ʹ��
class AuthorAdmin(admin.ModelAdmin):
    #list_display�� ����һ���ֶ����Ƶ�Ԫ�飬�����б���ʾ
    list_display = ('first_name', 'last_name', 'email')
    #���һ�����ٲ�ѯ��,��AuthorAdmin׷��search_fields
    search_fields = ('first_name', 'last_name')

class BookAdmin(admin.ModelAdmin):
    #list_display����ʹ��ҳ��ÿ�Щ
    list_display = ('title', 'publisher', 'publication_date')
    #��list_filter����������������Ϊ�������ֶ��ṩ�˿�ݹ��˷�ʽ�������������졢�������졢���ºͽ���
    list_filter = ('publication_date',)
    #��������, �ӿ��õ���ݿ�ʼȻ�����ϸ�ֵ���������
    date_hierarchy = 'publication_date'
    #�ı�Ĭ�ϵ�����ʽ����publication date��������
    ordering = ('-publication_date',)
    #�Զ����ֶ�˳�� Ĭ���ֶ�˳������ģ���ж�����һ�µ�,����ͨ��ʹ��ModelAdmin�����е�fieldsѡ�����ı���
    fields = ('title', 'authors', 'publisher', 'publication_date')
    #ʵ��Author����һ�����ɵ�JavaScript������������ѡ��authors��Available���Ƶ�Chosen�򣬻������ƻ���
    filter_horizontal = ('authors',)
    #������������ֶ����Ƶ�Ԫ�飬���������ֶν���չ�ֳ��ı��򣬲���ϵͳĬ�ϵ�������
    #raw_id_fields = ('publisher',)


admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)