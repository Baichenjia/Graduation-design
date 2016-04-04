# -*- coding: cp936 -*-
from django.http import HttpResponse
from django.http import Http404
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
import datetime
import MySQLdb


def hello(request):
	return HttpResponse("Hello world")


def current_datetime(requset):
	"""
	now = datetime.datetime.now()
	t = get_template('current_datetime.html')
	html = t.render(Context({'current_date': now}))
	return HttpResponse(html)
	"""
	"""
	now = datetime.datetime.now()
	return render_to_response('current_datetime.html', {'current_date': now})
	"""
	current_date = datetime.datetime.now()
	return render_to_response('current_datetime.html', locals())

def hours_ahead(request, offset):
	"""
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
	return HttpResponse(html)
	"""
	"""
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	return render_to_response("hours_ahead.html",{'hour_offset':offset, 'next_time':dt})
	"""
	try:
		hour_offset = int(offset)
	except ValueError:
		raise Http404()
	next_time = datetime.datetime.now() + datetime.timedelta(hours=hour_offset)
	return render_to_response("hours_ahead.html", locals())


def book_list(request):
	#ԭʼ�ķ��������ݿ����Ӳ���Ӳ�б����ڴ���֮��
	db = MySQLdb.connect(user='root', db='test', passwd='640120', host='localhost')        # �������ݿ�����
	cursor = db.cursor()                                       # �������ݿ��α�
	cursor.execute('SELECT * FROM book ORDER BY name')   # ִ��SQL���
	names = [row[0] for row in cursor.fetchall()]
	db.close()                           # �ر����ݿ�
	return render_to_response("book_list.html", {'names':names})   # ���أ�ָ��HTMLģ��









