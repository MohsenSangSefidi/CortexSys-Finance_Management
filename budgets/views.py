from django.db import IntegrityError

from utils.polls import authenticate_jwt_token
from rest_framework.response import Response
from rest_framework import views, status

from budgets.serializers import BudgetSerializer, UpdateBudgetSerializer

from .models import BudgetModel


class BudgetView(views.APIView):
    def get(self, request, *args, **kwargs):
        # Validate user authentications
        jwt_token = request.COOKIES.get("access_token")

        result, response, user = authenticate_jwt_token(jwt_token)

        if result:
            return response

        budgets = BudgetModel.objects.filter(user=user)

        serializer = BudgetSerializer(budgets, many=True)

        return Response(
            {"result": True, "massage": "successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        # Validate user authentications
        jwt_token = request.COOKIES.get("access_token")

        result, response, user = authenticate_jwt_token(jwt_token)

        if result:
            return response

        # Validate data
        serializer = BudgetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"result": False, "massage": "Invalid data", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Data
        title = serializer.validated_data.get("title")
        total_amount = serializer.validated_data.get("total_amount")
        start_date = serializer.validated_data.get("start_date")
        end_date = serializer.validated_data.get("end_date")

        # Create Budget
        try:
            budget = BudgetModel.objects.create(
                title=title,
                total_amount=total_amount,
                start_date=start_date,
                end_date=end_date,
                user_id=user.id,
            )
        except IntegrityError:
            return Response(
                {"result": False, "massage": "Invalid data", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Return response and data
        return Response(
            {
                "result": True,
                "massage": "Created budget successfully",
                "data": [BudgetSerializer(budget).data],
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, *args, **kwargs):
        # Validate user authentications
        jwt_token = request.COOKIES.get("access_token")

        result, response, user = authenticate_jwt_token(jwt_token)

        if result:
            return response

        # Validate data
        serializer = UpdateBudgetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"result": False, "massage": "Invalid data", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Data
        budget_id = serializer.validated_data.get("id")
        title = serializer.validated_data.get("title")
        total_amount = serializer.validated_data.get("total_amount")
        start_date = serializer.validated_data.get("start_date")
        end_date = serializer.validated_data.get("end_date")

        # Get Budget
        try:
            budget = BudgetModel.objects.get(id=budget_id, user_id=user.id)
        except BudgetModel.DoesNotExist:
            return Response(
                {"result": False, "massage": "Budget does not exist", "data": []},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update budget
        budget.title = title if title else budget.title
        budget.total_amount = total_amount if total_amount else budget.total_amount
        budget.start_date = start_date if start_date else budget.start_date
        budget.end_date = end_date if end_date else budget.end_date

        budget.save()  # Save

        return Response(
            {
                "result": True,
                "massage": "Updated budget successfully",
                "data": [BudgetSerializer(budget).data],
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        # Validate user authentications
        jwt_token = request.COOKIES.get("access_token")

        result, response, user = authenticate_jwt_token(jwt_token)

        if result:
            return response

        # Validate data
        serializer = UpdateBudgetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"result": False, "massage": "Invalid data", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Data
        budget_id = serializer.validated_data.get("id")

        # Get budget
        try:
            budget = BudgetModel.objects.get(id=budget_id, user_id=user.id)
        except BudgetModel.DoesNotExist:
            return Response(
                {"result": False, "massage": "Budget does not exist", "data": []},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete budget
        budget.delete()

        return Response(
            {"result": True, "massage": "Deleted budget successfully", "data": []},
            status=status.HTTP_200_OK,
        )
