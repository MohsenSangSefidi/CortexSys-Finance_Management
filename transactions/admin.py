from django.contrib import admin
from .models import TransactionModel


class TransactionAdmin(admin.ModelAdmin):
    list_display = ["title", "amount", "type", "date"]


admin.site.register(TransactionModel, TransactionAdmin)
