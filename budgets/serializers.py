from rest_framework import serializers
from .models import BudgetModel


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetModel
        fields = "__all__"
        read_only_fields = ["id", "user"]


class UpdateBudgetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(required=False)
    total_amount = serializers.IntegerField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    class Meta:
        fields = ["id", "title", "total_amount", "start_date", "end_date"]
