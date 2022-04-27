from django.urls import path

from account.views import SignInView, SignUpView, LogoutView, ProfileView

urlpatterns = [
    # api url
    path('signin/', SignInView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view())
]
