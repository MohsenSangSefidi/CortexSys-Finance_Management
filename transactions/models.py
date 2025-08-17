from django.db import models
from accounts.models import UserModel


class TransactionModel(models.Model):
    type_choices = (('Income', 'Income'), ('Expense', 'Expense'))

    title = models.CharField(max_length=100)
    amount = models.IntegerField()
    type = models.CharField(choices=type_choices, max_length=7)
    date = models.DateField()
    notes = models.TextField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
