from django.urls import path
from . import views
from userssection import views as UsViews

urlpatterns = [
    path('',views.main_page,name='mainpage'),
    path('register',views.register_page,name='register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('explorepage',views.explore_page,name='explore'),
    path('notifications/', UsViews.notification_list, name='notifications'),
]