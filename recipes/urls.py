from django.urls import path
from .views import RecipeSearchView

app_name = 'recipes'

urlpatterns = [
    path('search/', RecipeSearchView.as_view(), name='search'),
]

