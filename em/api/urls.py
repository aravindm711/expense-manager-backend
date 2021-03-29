from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import CreateUserAPIView, LogoutUserAPIView
from .views import ExpenseViewSet

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    url(r'', include(router.urls)),                 # app urls from router
    # url(r"^expense/list/$", ExpenseListAPIView.as_view(), name="expense_list"),
    url(r"^auth/login/$", obtain_auth_token, name="auth_user_login"),
    url(r"^auth/register/$", CreateUserAPIView.as_view(), name="auth_user_create"),
    url(r"^auth/logout/$", LogoutUserAPIView.as_view(), name="auth_user_logout"),
]
