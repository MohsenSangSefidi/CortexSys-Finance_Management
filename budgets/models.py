from django.db import models
from accounts.models import UserModel


class BudgetModel(models.Model):
    title = models.CharField(max_length=100)
    total_amount = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
