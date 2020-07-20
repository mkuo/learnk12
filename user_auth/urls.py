from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('user-tutor/', views.create_tutor, name='user_tutor'),
    path('update_tutor/<int:tutor_id>', views.update_tutor, name='update_tutor'),
    path('all-user-tutor/', views.user_tutors, name='all_tutors')
]
