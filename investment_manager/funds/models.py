from django.db import models
from django.contrib.auth.models import User


class Fund(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FundPerformance(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    month = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.fund.name} - {self.month}"


class Investment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    initial_amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_month = models.CharField(max_length=50)
    end_month = models.CharField(max_length=50)
    final_value = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    def calculate_final_value(self):
        start_performance = FundPerformance.objects.get(
            fund=self.fund, month=self.start_month
        )
        end_performance = FundPerformance.objects.get(
            fund=self.fund, month=self.end_month
        )
        profit_rate = (
            end_performance.value - start_performance.value
        ) / start_performance.value
        self.final_value = self.initial_amount * (1 + profit_rate)
        self.save()

    def save(self, *args, **kwargs):
        if not self.final_value:
            self.calculate_final_value()
        super(Investment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.fund.name} Investment"
