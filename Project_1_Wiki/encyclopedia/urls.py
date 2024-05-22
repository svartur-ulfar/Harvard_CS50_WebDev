from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # Creating the EntryPage by creating a path
    # where TITLE is an expected string entry
    path("wiki/<str:title>", views.entry, name="entry"),

    # Creating path for search page result
    path("search/", views.search, name="search"),

    # Creating path for NewPage option
    path("newPage/", views.new_page, name="new_page"),

    # Create path for EditPage option
    path("editPage/", views.edit_page, name="edit_page"),

    # Create a path for SavedPage 
    path("save_page/", views.save_page, name="save_page"),

    # Create path for Random Page
    path("random_page/", views.random_page, name="random_page")

]
