from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new_page, name="new_page"),
    path("<str:title>/edit", views.edit_entry, name="edit_entry"),
    path("random/", views.random, name="random")
]
