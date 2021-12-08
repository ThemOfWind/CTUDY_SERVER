from django.urls import path

from account.views import SignInView, SignUpView, LogoutView

urlpatterns = [
    # api url
    path('signin/', SignInView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('logout/', LogoutView.as_view())
]
