from django.contrib import admin
from .models import Fund, FundPerformance, Investment


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    pass


@admin.register(FundPerformance)
class FundPerformanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    pass
