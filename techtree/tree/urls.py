from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tree_index'),
    path('dict/', views.treedict, name="tree_dict"),
]