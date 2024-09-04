from rest_framework import serializers
from .models import Fund, FundPerformance, Investment

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'

class FundPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundPerformance
        fields = '__all__'

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'
