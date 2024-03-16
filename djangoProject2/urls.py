from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import signup, home, list_users, delete_user, profile_view, login_view, logout_view
from .views import login_redirect_view

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', home, name='home'),
    path('login/', login_view, name='login'),  # Ajustado para usar a view de login personalizada
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('list_users/', list_users, name='list_users'),
    path('password_reset/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('password_reset/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),  # Removi a referência à página de login nesta rota
    path('accounts/login/', login_redirect_view, name='login_redirect'),
    path('password_reset/login/', login_redirect_view, name='login_redirect')
]