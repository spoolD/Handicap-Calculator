from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('add', views.add_score, name='add'),
    path('lookup', views.lookup, name='lookup'),
    path('search/<str:term>', views.search, name="search"),
    path('follow', views.follow, name='follow')
]