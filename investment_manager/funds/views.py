from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Fund, FundPerformance, Investment
from .serializer import FundSerializer, FundPerformanceSerializer, InvestmentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal


class Login(TokenObtainPairView):
    pass


class Refresh(TokenRefreshView):
    pass


class FundListCreateView(generics.ListCreateAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]


class FundPerformanceListCreateView(generics.ListCreateAPIView):
    queryset = FundPerformance.objects.all()
    serializer_class = FundPerformanceSerializer
    permission_classes = [IsAuthenticated]


class InvestmentListCreateView(generics.ListCreateAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvestmentHistoryView(generics.ListAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user)


class FundPerformanceCreateView(APIView):

    def post(self, request):
        data = request.data

        for fund_data in data.get("funds", []):

            fund, created = Fund.objects.get_or_create(name=fund_data["fund_name"])

            for month_data in fund_data["performances"]:
                FundPerformance.objects.create(
                    fund=fund, month=month_data["month"], value=month_data["value"]
                )

        return Response(
            {"message": "Data added successfully"}, status=status.HTTP_201_CREATED
        )


def find_best_investment_period(values, months):
    if not values or len(values) < 2:
        return None

    min_value = Decimal(values[0])
    min_index = 0
    max_return = Decimal("0.00")
    best_start_index = None
    best_end_index = None

    for i in range(1, len(values)):
        current_value = Decimal(values[i])

        potential_return = current_value - min_value

        if potential_return > max_return:
            max_return = potential_return
            best_start_index = min_index
            best_end_index = i

        if current_value < min_value:
            min_value = current_value
            min_index = i

    if best_start_index is not None and best_end_index is not None:
        return {
            "min_value": values[best_start_index],
            "max_value": values[best_end_index],
            "max_return": max_return,
            "best_start_month": months[best_start_index],
            "best_end_month": months[best_end_index],
        }
    else:
        return None


class BestInvestmentView(APIView):

    def get(self, request):
        best_periods = []
        best_fund = None
        highest_return = Decimal("-inf")

        funds = Fund.objects.all()
        for fund in funds:
            performances = FundPerformance.objects.filter(fund=fund)

            values = [performance.value for performance in performances]
            months = [performance.month for performance in performances]

            result = find_best_investment_period(values, months)

            if result:
                best_periods.append(
                    {
                        "fund": fund.name,
                        "best_start_month": result["best_start_month"],
                        "best_end_month": result["best_end_month"],
                        "min_value": result["min_value"],
                        "max_value": result["max_value"],
                        "max_return": result["max_return"],
                    }
                )

                if result["max_return"] > highest_return:
                    highest_return = result["max_return"]
                    best_fund = {
                        "fund": fund.name,
                        "best_start_month": result["best_start_month"],
                        "best_end_month": result["best_end_month"],
                        "min_value": result["min_value"],
                        "max_value": result["max_value"],
                        "max_return": result["max_return"],
                    }

        return Response(
            {"best_periods": best_periods, "most_efficient_fund": best_fund},
            status=status.HTTP_200_OK,
        )


class MostEfficientInvestmentView(APIView):

    def get(self, request):
        user = request.user
        investments = Investment.objects.filter(user=user)

        best_investment = None
        highest_return = Decimal("-inf")

        for investment in investments:
            start_performance = FundPerformance.objects.get(
                fund=investment.fund, month=investment.start_month
            )
            end_performance = FundPerformance.objects.get(
                fund=investment.fund, month=investment.end_month
            )
            start_value = start_performance.value
            end_value = end_performance.value

            profit_rate = (end_value - start_value) / start_value
            final_value = investment.initial_amount * (1 + profit_rate)
            return_amount = final_value - investment.initial_amount

            if return_amount > highest_return:
                highest_return = return_amount
                best_investment = {
                    "fund": investment.fund.name,
                    "start_month": investment.start_month,
                    "end_month": investment.end_month,
                    "initial_amount": investment.initial_amount,
                    "final_value": final_value,
                    "return_amount": return_amount,
                }

        return Response(
            {"most_efficient_investment": best_investment}, status=status.HTTP_200_OK
        )
