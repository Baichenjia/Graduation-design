# -*- coding: cp936 -*-
__author__ = 'Bai Chenjia'

from django.contrib import admin
from mysite.books.models import Publisher, Author, Book

#AuthorAdmin从django.contrib.admin.ModelAdmin派生出来的子类，保存着一个类的自定义配置，以供管理工具使用
class AuthorAdmin(admin.ModelAdmin):
    #list_display， 它是一个字段名称的元组，用于列表显示
    list_display = ('first_name', 'last_name', 'email')
    #添加一个快速查询栏,向AuthorAdmin追加search_fields
    search_fields = ('first_name', 'last_name')

class BookAdmin(admin.ModelAdmin):
    #list_display，以使得页面好看些
    list_display = ('title', 'publisher', 'publication_date')
    #用list_filter创建过滤器，并且为日期型字段提供了快捷过滤方式，它包含：今天、过往七天、当月和今年
    list_filter = ('publication_date',)
    #过滤日期, 从可用的年份开始然后逐层细分到月乃至日
    date_hierarchy = 'publication_date'
    #改变默认的排序方式，按publication date降序排列
    ordering = ('-publication_date',)
    #自定义字段顺序。 默认字段顺序是与模块中定义是一致的,可以通过使用ModelAdmin子类中的fields选项来改变它
    fields = ('title', 'authors', 'publisher', 'publication_date')
    #实现Author区的一个精巧的JavaScript过滤器，可以选中authors从Available框移到Chosen框，还可以移回来
    filter_horizontal = ('authors',)
    #操作包含外键字段名称的元组，它包含的字段将被展现成文本框，不是系统默认的下拉框
    #raw_id_fields = ('publisher',)


admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)