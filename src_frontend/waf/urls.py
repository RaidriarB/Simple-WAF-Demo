from django.urls import path,re_path

from . import views

urlpatterns = [
    path('',views.EmptyView.as_view(),name='empty'),
	# path('index',views.IndexView.as_view(),name='index'),
    path('log',views.LogView.as_view(),name='log'),
    re_path(r'^log_del-(?P<nid>\d+)/', views.log_del),
    re_path(r'^log_detail-(?P<nid>\d+)/', views.log_detail),
    # path('table',views.LogView.as_view(),name='rule'),
    # path('form',views.FormView.as_view(),name='form'),
    # path('ui-elements',views.UIElementsView.as_view(),name='ui-elements'),
    # path('chart',views.ChartView.as_view(),name='chart'),
    path('empty',views.EmptyView.as_view(),name='empty'),
    # path('tab-panel',views.TabPanelView.as_view(),name='tab-panel'),
    path('rule',views.RuleView.as_view(),name= 'rule'),
    re_path(r'^rule_del-(?P<nid>\d+)/', views.rule_del),
    re_path(r'^rule_edit-(?P<nid>\d+)/', views.rule_edit),
    path('rule_create',views.rule_create),
    path('Whitelist',views.WhitelistView.as_view(),name= 'Whitelist'),
    re_path(r'^Whitelist_del-(?P<nid>\d+)/', views.Whitelist_del),
    re_path(r'^Whitelist_edit-(?P<nid>\d+)/', views.Whitelist_edit),
    path('Whitelist_create',views.Whitelist_create),
    path('Blacklist',views.BlacklistView.as_view(),name= 'Blacklist'),
    re_path(r'^Blacklist_del-(?P<nid>\d+)/', views.Blacklist_del),
    re_path(r'^Blacklist_edit-(?P<nid>\d+)/', views.Blacklist_edit),
    path('Blacklist_create',views.Blacklist_create)
]