from rest_framework import serializers
from .models import TransactionModel


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = "__all__"
        read_only_fields = ("id", "created_at", "user")


class UpdateTransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(required=False)
    amount = serializers.IntegerField(required=False)
    type = serializers.ChoiceField(
        choices=TransactionModel.type_choices, required=False
    )
    date = serializers.DateField(required=False)
    notes = serializers.CharField(required=False)

    class Meta:
        fields = ["id", "title", "amount", "type", "date", "notes"]
