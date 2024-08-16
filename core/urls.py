from django.urls import path, include
from core.views import HomeView
urlpatterns = [
    path("", HomeView, name="home"),
    path('category/<slug:slug>', HomeView, name='category_wise_book')
]