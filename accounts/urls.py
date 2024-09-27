from django.urls import path

from accounts.views import UserRegistrations, UserLoginView, UserLogoutView

urlpatterns = [
    path('registration/', UserRegistrations.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),

]
