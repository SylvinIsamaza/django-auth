from django.urls import path
from .views import LoginView, UserView,RegisterView, LogoutView,homePageView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('', homePageView,name="index")
]
