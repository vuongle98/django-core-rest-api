from django.urls import path
from core.auth.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('/login/', LoginView.as_view(), name='login'),

]