from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
