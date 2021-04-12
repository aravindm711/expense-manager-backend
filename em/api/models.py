from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

import uuid
import datetime

User._meta.get_field("email")._unique = True


class Expense(models.Model):
    CASH = "CS"
    CARD = "CR"
    TYPE_OF_PAYMENT = [(CASH, "Cash"), (CARD, "Card")]

    GROCERY = "GROCERY"
    MEDICINE = "MEDICINE"
    FOOD = "FOOD"
    TRAVEL = "TRAVEL"
    OTHER = "OTHER"
    CLOTHING = "CLOTHING"
    HOBBY = "HOBBY"
    RESTAURANT = "RESTAURANT"
    UTILITY = "UTILITY"
    PERSONAL = "PERSONAL"
    EDUCATION = "EDUCATION"
    ENTERTAINMENT = "ENTERTAINMENT"
    TAGS = [
        (GROCERY, "Grocery"),
        (MEDICINE, "Medicine"),
        (FOOD, "Food"),
        (TRAVEL, "Travel"),
        (CLOTHING, "Clothing"),
        (HOBBY, "Hobby"),
        (RESTAURANT, "Restaurant"),
        (UTILITY, "Utility"),
        (PERSONAL, "Personal"),
        (EDUCATION, "Education"),
        (ENTERTAINMENT, "Entertainment"),
        (OTHER, "Other"),
    ]

    expense_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=datetime.date.today, null=False, blank=False)
    amount = models.IntegerField(default=0, null=False, blank=False)
    detail = models.CharField(max_length=30, blank=True, null=True)
    payment_type = models.CharField(max_length=2, choices=TYPE_OF_PAYMENT, default=CASH)
    tags = models.CharField(max_length=15, choices=TAGS, default=OTHER)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(
        get_user_model(), null=False, blank=False, on_delete=models.CASCADE
    )


class LentOrOwedExpense(models.Model):
    CASH = "CS"
    CARD = "CR"
    TYPE_OF_PAYMENT = [(CASH, "Cash"), (CARD, "Card")]

    GROCERY = "GROCERY"
    MEDICINE = "MEDICINE"
    FOOD = "FOOD"
    TRAVEL = "TRAVEL"
    OTHER = "OTHER"
    CLOTHING = "CLOTHING"
    HOBBY = "HOBBY"
    RESTAURANT = "RESTAURANT"
    UTILITY = "UTILITY"
    PERSONAL = "PERSONAL"
    EDUCATION = "EDUCATION"
    ENTERTAINMENT = "ENTERTAINMENT"
    TAGS = [
        (GROCERY, "Grocery"),
        (MEDICINE, "Medicine"),
        (FOOD, "Food"),
        (TRAVEL, "Travel"),
        (CLOTHING, "Clothing"),
        (HOBBY, "Hobby"),
        (RESTAURANT, "Restaurant"),
        (UTILITY, "Utility"),
        (PERSONAL, "Personal"),
        (EDUCATION, "Education"),
        (ENTERTAINMENT, "Entertainment"),
        (OTHER, "Other"),
    ]

    expense_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=datetime.date.today, null=False, blank=False)
    amount = models.IntegerField(default=0, null=False, blank=False)
    detail = models.CharField(max_length=30, blank=True, null=True)
    payment_type = models.CharField(max_length=2, choices=TYPE_OF_PAYMENT, default=CASH)
    tags = models.CharField(max_length=15, choices=TAGS, default=OTHER)
    to = models.CharField(max_length=30, null=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(
        get_user_model(), null=False, blank=False, on_delete=models.CASCADE
    )


class ExpenseNotification(models.Model):
    NEW = "NEW"
    READ = "READ"
    NOTIF_CH = [(NEW, "New"), (READ, "Read")]

    notif_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detail = models.CharField(max_length=200, null=False)
    notified = models.CharField(max_length=4, choices=NOTIF_CH, default=NEW)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    to = models.ForeignKey(
        get_user_model(), null=False, blank=False, on_delete=models.CASCADE
    )
