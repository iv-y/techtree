from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='tree_index'),
    path('dict/', views.treedict, name="tree_dict"),
    path('dict/<str:department_code>/', views.treedict, name="tree_dict_code"),
    
    path('a/c/<str:c_code>/<str:a_full_name>/', views.treedict_alias_create, name="tree_dict_ac"),
    path('a/l/<int:a_id>/', views.treedict_alias_like, name="tree_dict_al"),
    path('p/c/<str:c_p_code>/<str:c_c_code>/', views.treedict_prerequisite_create, name="tree_dict_pc"),
    path('p/l/<int:p_id>/', views.treedict_prerequisite_like, name="tree_dict_pl"),
    
]