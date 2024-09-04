from django.urls import path
from .views import (
    FundListCreateView,
    FundPerformanceListCreateView,
    InvestmentListCreateView,
    InvestmentHistoryView,
    BestInvestmentView,
    MostEfficientInvestmentView,
)
from .views import FundPerformanceCreateView

urlpatterns = [
    path("funds/", FundListCreateView.as_view(), name="fund-list-create"),
    path(
        "performances/",
        FundPerformanceListCreateView.as_view(),
        name="fund-performance-list-create",
    ),
    path(
        "investments/",
        InvestmentListCreateView.as_view(),
        name="investment-list-create",
    ),
    path(
        "investment-history/",
        InvestmentHistoryView.as_view(),
        name="investment-history",
    ),
    path(
        "create-fund-performance/",
        FundPerformanceCreateView.as_view(),
        name="create-fund-performance",
    ),
    path("best-investment/", BestInvestmentView.as_view(), name="best-investment"),
    path(
        "most-efficient-investment/",
        MostEfficientInvestmentView.as_view(),
        name="most-efficient-investment",
    ),
]
