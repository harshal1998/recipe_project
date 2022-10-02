from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    path("",home),
    path('registration', registration),
    path('login',login),
    path('logout',logout),
    path('recipe_detail/<id>',recipe_detail),
    path('add',add_recipe.as_view()),
    path('edit/<id>',edit_recipe.as_view()),
    path('recipe/<id>',view_recipe),
    path('search',search),
]
