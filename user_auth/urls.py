from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('update-profile/', views.update_profile, name='update_profile')
]
