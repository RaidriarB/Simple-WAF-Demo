from django.urls import path

from . import views

urlpatterns = [
	path('index',views.IndexView.as_view(),name='index'),
    path('log',views.LogView.as_view(),name='log'),
    path('table',views.LogView.as_view(),name='rule'),
    path('form',views.FormView.as_view(),name='form'),
    path('ui-elements',views.UIElementsView.as_view(),name='ui-elements'),
    path('chart',views.ChartView.as_view(),name='chart'),
    path('empty',views.EmptyView.as_view(),name='empty'),
    path('tab-panel',views.TabPanelView.as_view(),name='tab-panel')
]