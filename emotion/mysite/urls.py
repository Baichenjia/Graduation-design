# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from mysite.books.models import *

admin.autodiscover()

# publisher 页面实现的内容，指定模板
publisher_info = {
    'queryset': Publisher.objects.all(),
    'template_name': 'publisher_list_page.html',
}


urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    ('^hello/$',  'mysite.views.hello'),
    ('^time/$', 'mysite.views.current_datetime'),
    (r'^time/plus/(\d{1,2})/$', 'mysite.views.hours_ahead'),
    ('^book/$', 'mysite.views.book_list'),
    ('^search/$', 'mysite.books.views.search'),
    ('^contact/$', 'mysite.books.views.contact_new'),
    ('^contact/thanks/$', 'mysite.books.views.thanks'),
    (r'^publishers/$', list_detail.object_list, publisher_info),
    (r'^login/$', 'mysite.books.views.login'),
    (r'^images/(?P<path>.*)', 'django.views.static.serve', {'document_root': 'F:/emotion/mysite/static/images'}),
    (r'^register/$','mysite.books.views.register'),
    (r'^emotion_steps_index/$', 'mysite.books.views.emotion_steps_index'),
    (r'^emotion_steps_1/$', 'mysite.books.views.emotion_steps_1'),
    (r'^emotion_steps_2/$', 'mysite.books.views.emotion_steps_2'),
    (r'^emotion_steps_3/$', 'mysite.books.views.emotion_steps_3'),
    (r'^emotion_steps_4/$', 'mysite.books.views.emotion_steps_4'),
    (r'^emotion_steps_5/$', 'mysite.books.views.emotion_steps_5'),
    (r'^form_crawler/$', 'mysite.books.views.form_crawler'),
    (r'^dic_pos_all/$', 'mysite.books.views.dic_pos_all'),
    (r'^dic_neg_all/$', 'mysite.books.views.dic_neg_all'),
    (r'^dic_pos_a/$', 'mysite.books.views.dic_pos_a'),
    (r'^dic_pos_b/$', 'mysite.books.views.dic_pos_b'),
    (r'^dic_pos_d/$', 'mysite.books.views.dic_pos_d'),
    (r'^dic_pos_i/$', 'mysite.books.views.dic_pos_i'),
    (r'^dic_pos_l/$', 'mysite.books.views.dic_pos_l'),
    (r'^dic_pos_n/$', 'mysite.books.views.dic_pos_n'),
    (r'^dic_pos_v/$', 'mysite.books.views.dic_pos_v'),
    (r'^dic_pos_z/$', 'mysite.books.views.dic_pos_z'),
    (r'^dic_neg_a/$', 'mysite.books.views.dic_neg_a'),
    (r'^dic_neg_b/$', 'mysite.books.views.dic_neg_b'),
    (r'^dic_neg_d/$', 'mysite.books.views.dic_neg_d'),
    (r'^dic_neg_i/$', 'mysite.books.views.dic_neg_i'),
    (r'^dic_neg_l/$', 'mysite.books.views.dic_neg_l'),
    (r'^dic_neg_n/$', 'mysite.books.views.dic_neg_n'),
    (r'^dic_neg_v/$', 'mysite.books.views.dic_neg_v'),
    (r'^dic_neg_z/$', 'mysite.books.views.dic_neg_z'),
    (r'^dic_but_word/$', 'mysite.books.views.dic_but_word'),
    (r'^dic_no_word/$', 'mysite.books.views.dic_no_word'),
    (r'^jixing_get_zhuguan', 'mysite.books.views.jixing_get_zhuguan'),   # 第三页开始
    (r'^jixing_get_xiangliang', 'mysite.books.views.jixing_get_xiangliang'),
    (r'^jixing_get_results', 'mysite.books.views.jixing_get_results'),
    (r'^dic_level_one', 'mysite.books.views.dic_level_one'),    # 第四页开始
    (r'^dic_level_two', 'mysite.books.views.dic_level_two'),
    (r'^dic_level_three', 'mysite.books.views.dic_level_three'),
    (r'^dic_level_four', 'mysite.books.views.dic_level_four'),
    (r'^dic_level_five', 'mysite.books.views.dic_level_five'),
    (r'^dic_level_six', 'mysite.books.views.dic_level_six'),
    (r'^dic_get_result', 'mysite.books.views.dic_get_result'),
    (r'^dic_get_analysis', 'mysite.books.views.dic_get_analysis'),
    (r'^ag1_tfidf_result', 'mysite.books.views.ag1_tfidf_result'),  # 第五页开始
    (r'^ag1_tfidf_label', 'mysite.books.views.ag1_tfidf_label'),
    (r'^ag2_textrank_score', 'mysite.books.views.ag2_textrank_score'),
    (r'^ag2_textrank_label', 'mysite.books.views.ag2_textrank_label'),
    (r'^ag3_hit_corpus', 'mysite.books.views.ag3_hit_corpus'),
    (r'ag3_cluster_label', 'mysite.books.views.ag3_cluster_label'),

)
