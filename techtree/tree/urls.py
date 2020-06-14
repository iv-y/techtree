from django.urls import path

from . import views
from . import signupviews

urlpatterns = [
    path('accounts/signup/', signupviews.CreateUserView.as_view(), name='signup'),
    path('accounts/login/done', signupviews.RegisteredView.as_view(), name="create_user_done"),
    path('', views.index, name='tree_index'),
    path('dict/', views.treedict, name="tree_dict"),
]