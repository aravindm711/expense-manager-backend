from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    CreateUserAPIView,
    LogoutUserAPIView,
    ExpenseViewSet,
    LentOrOwedExpenseViewSet,
    ExpenseNotificationViewSet,
)

router = DefaultRouter()
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(r"lentorowedexpenses", LentOrOwedExpenseViewSet, basename="lentorowedexpense")
router.register(r"notifications", ExpenseNotificationViewSet, basename="notification")

urlpatterns = [
    url(r"", include(router.urls)),  # app urls from router
    url(r"^auth/login/$", obtain_auth_token, name="auth_user_login"),
    url(r"^auth/register/$", CreateUserAPIView.as_view(), name="auth_user_create"),
    url(r"^auth/logout/$", LogoutUserAPIView.as_view(), name="auth_user_logout"),
]
