from django.urls import path

from account.views import SignInView

urlpatterns = [
    # api url
    path('signin/', SignInView.as_view()),
]
