from django.db import IntegrityError
from rest_framework.response import Response
from utils.polls import authenticate_jwt_token
from rest_framework import views, status

from transactions.serializers import TransactionSerializer, UpdateTransactionSerializer

from .models import TransactionModel


class TransactionView(views.APIView):
    def get(self, request, *args, **kwargs):
        jwt_token = request.COOKIES.get("access_token")

        result, response, user = authenticate_jwt_token(jwt_token)

        if result:
            return response

        # Get transactions
        transactions_list = user.transactions.all()
        data = TransactionSerializer(transactions_list, many=True)

        return Response(
            {
                "result": True,
                "message": "success",
                "data": data.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        # Validate user authentications
        jwt_token = request.COOKIES.get("access_token")

        result, response, user = authenticate_jwt_token(jwt_token)

        if result:
            return response

        # Validating user data
        serializer = TransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"result": False, "message": "Invalid data", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set Data
        title = serializer.validated_data.get("title")
        amount = serializer.validated_data.get("amount")
        transaction_type = serializer.validated_data.get("type")
        date = serializer.validated_data.get("date")
        notes = serializer.validated_data.get("notes")

        # Create transaction
        try:
            transaction = TransactionModel.objects.create(
                title=title,
                amount=amount,
                type=transaction_type,
                date=date,
                notes=notes,
                user_id=user.id,
            )
        except IntegrityError:
            return Response(
                {"result": False, "message": "creating failed", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "result": True,
                "message": "Transaction created",
                "data": [TransactionSerializer(transaction).data],
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, *args, **kwargs):
        # Validate user authentications
        jwt_token = request.COOKIES.get("access_token")

        result, response, user = authenticate_jwt_token(jwt_token)

        if result:
            return response

        # Validating user data
        serializer = UpdateTransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"result": False, "message": "Invalid data", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Data
        transaction_id = serializer.validated_data.get("id")
        title = serializer.validated_data.get("title")
        amount = serializer.validated_data.get("amount")
        transaction_type = serializer.validated_data.get("type")
        date = serializer.validated_data.get("date")
        notes = serializer.validated_data.get("notes")

        # Get Transaction
        try:
            transaction = TransactionModel.objects.get(
                id=transaction_id, user_id=user.id
            )
        except TransactionModel.DoesNotExist:
            return Response(
                {"result": False, "message": "Transaction does not exist", "data": []},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update Transaction ( If data is None not replaced )
        transaction.title = title if title else transaction.title
        transaction.amount = amount if amount else transaction.amount
        transaction.type = transaction_type if transaction_type else transaction.type
        transaction.date = date if date else transaction.date
        transaction.notes = notes if notes else transaction.notes

        transaction.save()  # Save

        # Return Response
        return Response(
            {
                "result": True,
                "message": "Transaction updated",
                "data": [TransactionSerializer(transaction).data],
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        # Validate user authentications
        jwt_token = request.COOKIES.get("access_token")

        result, response, user = authenticate_jwt_token(jwt_token)

        if result:
            return response

        # Validating user data
        serializer = UpdateTransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"result": False, "message": "Invalid data", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Data
        transaction_id = serializer.validated_data.get("id")

        # Get Transaction
        try:
            transaction = TransactionModel.objects.get(
                id=transaction_id, user_id=user.id
            )
        except TransactionModel.DoesNotExist:
            return Response(
                {"result": False, "message": "Transaction does not exist", "data": []},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete Transaction
        transaction.delete()

        return Response(
            {"result": True, "message": "Transaction deleted", "data": []},
            status=status.HTTP_200_OK,
        )
