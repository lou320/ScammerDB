from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm

urlpatterns = [
    path('', views.scammer_list, name='scammer_list'),
    path('scammer/<int:pk>/', views.scammer_detail, name='scammer_detail'),
    path('add/', views.add_scammer, name='add_scammer'),
    path('scammer/<int:pk>/approve/', views.approve_scammer, name='approve_scammer'),
    path('scammer/<int:pk>/reject/', views.reject_scammer, name='reject_scammer'),
    path('pending/', views.pending_scammers, name='pending_scammers'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='scammers/login.html', form_class=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('scammer/<int:pk>/purchase/', views.purchase_access, name='purchase_access'),
]
