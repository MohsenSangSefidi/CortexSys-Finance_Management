from django.contrib import admin
from .models import BudgetModel


class BudgetAdmin(admin.ModelAdmin):
    list_display = ("title", "total_amount")


admin.site.register(BudgetModel, BudgetAdmin)
