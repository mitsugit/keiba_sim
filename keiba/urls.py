from django.conf.urls import url
# #from .views import HelloView
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('',views.home,name=''),
    path('index',views.index,name='index'),
    path('racesettei',views.racesettei,name='racesettei'),
    path('logic',views.logic,name='logic'),
    path('result',views.result,name='result'),
    path('racerecord',views.racerecord,name='racerecord'),
    path('logic_save',views.logic_save,name='logic_save'),
    # path('logicedit/<int:num>',views.logicedit,name='logicedit'),
    path('logic_list',views.logic_list,name='logic_list'),
    path('session_count',views.session_count,name='session_count'),
    path('session_flush',views.session_flush,name='session_flush'),
    path('login',views.login_view,name='login'),
    path('create_user',views.create_user,name='create_user'),
    path('create_user_view',views.create_user_view,name='create_user_view'),
    path('accounts/login',LoginView.as_view(template_name='login_view.html')),
    path('logout',views.logout_view),
    path('forquestion',views.forquestion,name='forquestion'),
]
