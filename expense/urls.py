from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signup/', views.signupUser, name='signup'),
    path('login/', views.loginUser, name='login'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('logout/', views.logoutUser, name='logout'),
    path('userhome/', views.userhome, name='userhome'),
    path('usertransactions/',views.usertransactions, name = 'usertransactions'),
    path('addtransaction/',views.addtransaction, name = 'addtransaction'),
    path('exporttransaction/',views.exporttransaction, name = 'exporttransaction'),
    path('analysis/',views.analysis, name = 'analysis'),
]