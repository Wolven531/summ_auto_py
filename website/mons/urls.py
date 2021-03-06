"""
	This is the urls module
"""
from django.urls import path
from . import views

app_name = 'mons'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('load', views.load_monsters, name='load')
]
