import copy

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api.serializers import (
    CreateUserSerializer,
    ExpenseSerializer,
    LentOrOwedExpenseSerializer,
    ExpenseNotificationSerializer,
)

from .models import Expense, LentOrOwedExpense, ExpenseNotification


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # We create a token than will be used for future auth
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ExpenseViewSet(ModelViewSet):
    serializer_class = ExpenseSerializer

    lookup_field = "expense_id"

    def get_queryset(self):
        return Expense.objects.filter(created_by=self.request.user).order_by("-date")

    def create(self, request, *args, **kwargs):
        data = copy.deepcopy(request.data)
        data["created_by"] = get_user_model().objects.get(username=request.user).pk
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)

        return Response(
            {**serializer.data}, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = copy.deepcopy(request.data)
        data["created_by"] = get_user_model().objects.get(username=request.user).pk
        print(data)
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)

        return Response(
            {**serializer.data}, status=status.HTTP_202_ACCEPTED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(status=status.HTTP_200_OK)


class LentOrOwedExpenseViewSet(ModelViewSet):
    serializer_class = LentOrOwedExpenseSerializer

    lookup_field = "expense_id"

    def get_queryset(self):
        return LentOrOwedExpense.objects.filter(
            Q(created_by=self.request.user) | Q(to=self.request.user)
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for i in range(len(serializer.data)):
            serializer.data[i]["created_by"] = (
                get_user_model()
                .objects.get(pk=serializer.data[i]["created_by"])
                .username
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if request.data["to"] != str(request.user):
            created_by = get_user_model().objects.get(username=request.user)
            data = copy.deepcopy(request.data)
            data["created_by"] = created_by.pk
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            if data["amount"] >= 0:
                det = "{} owed to {} for {}".format(
                    data["amount"], created_by, data["detail"]
                )
            else:
                det = "{} lent to {} for {}".format(
                    data["amount"], created_by, data["detail"]
                )
            if data["detail"] == "settle":
                det = "Settled {} to {}".format(data["amount"], created_by)
            to = get_user_model().objects.get(username=data["to"])
            ExpenseNotification.objects.create(to=to, detail=det)

            data = copy.deepcopy(serializer.data)
            data.update({'created_by': str(request.user)})

            return Response(
                {**data}, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        created_by = get_user_model().objects.get(username=request.user)
        amount_before = instance.amount
        data = copy.deepcopy(request.data)
        data["created_by"] = get_user_model().objects.get(username=request.user).pk
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        det = "{} updated to {} by {}".format(amount_before, data["amount"], created_by)
        to = get_user_model().objects.get(username=data["to"])
        ExpenseNotification.objects.create(to=to, detail=det)

        data = copy.deepcopy(serializer.data)
        data.update({'created_by': str(request.user)})

        return Response(
            {**serializer.data}, status=status.HTTP_202_ACCEPTED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to != str(request.user):
            instance.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ExpenseNotificationViewSet(ModelViewSet):
    serializer_class = ExpenseNotificationSerializer

    lookup_field = "notif_id"

    def get_queryset(self):
        return ExpenseNotification.objects.filter(to=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {}
        data["to"] = get_user_model().objects.get(username=request.user).pk
        data["notified"] = "READ"
        data["detail"] = instance.detail
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {**serializer.data}, status=status.HTTP_202_ACCEPTED, headers=headers
        )
