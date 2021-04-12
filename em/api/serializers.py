from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Expense, LentOrOwedExpense, ExpenseNotification


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ("username", "password", "email")
        write_only_fields = "password"
        read_only_fields = (
            "is_staff",
            "is_superuser",
            "is_active",
        )

    def create(self, validated_data):
        print(validated_data)
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["expense_id", "date", "amount", "detail", "payment_type", "tags"]


class LentOrOwedExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LentOrOwedExpense
        fields = [
            "expense_id",
            "to",
            "created_by",
            "date",
            "amount",
            "detail",
            "payment_type",
            "tags",
        ]


class ExpenseNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseNotification
        fields = ["notif_id", "detail", "notified", "created_on"]
