from django.urls import path
from .views import SignupView, CompleteProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/complete/', CompleteProfileView.as_view(), name='complete_profile'),
]