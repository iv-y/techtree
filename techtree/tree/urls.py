from django.urls import path

from . import views
from . import signupviews

urlpatterns = [
    path('accounts/signup/', signupviews.CreateUserView.as_view(), name='signup'),
    path('accounts/login/done', signupviews.RegisteredView.as_view(), name="create_user_done"),
    path('', views.index, name='tree_index'),
    path('alias/toggle/<str:c_code>/<int:a_id>/<int:uncheck>', views.treedict_alias_toggle, name='tree_dict_alias_toggle'),
    path('alias/create/<str:c_code>/<str:a_full_name:>', views.treedict_alias_create, name='tree_dict_alias_create'),
    path('prerequisite/toggle/<str:c_code>', views.treedict_prerequisite_toggle, name='tree_dict_prerequisite_toggle'),
    path('prerequisite/create/<str:c_code>', views.treedict_prerequisite_create, name='tree_dict_prerequisite_create'),
    path('dict/', views.treedict, name="tree_dict"),
    path('dict/<str:department_code>/', views.treedict, name="tree_dict_code"),
]