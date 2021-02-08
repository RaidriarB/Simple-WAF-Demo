from django.urls import path

from . import views

urlpatterns = [
	path('',views.IndexView.as_view(),name='index'),
    path('log',views.LogView.as_view(),name='log'),
    path('',views.RuleView.as_view(),name='rule'),
]