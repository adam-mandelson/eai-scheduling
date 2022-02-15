from django.db import models


class Report(models.Model):
    employeeName = models.CharField(max_length=50, blank=False, null=False)
    month = models.CharField(max_length=50, blank=False, null=False)
    dataTypes = models.CharField(max_lengh=50, blank=False, null=False)
    value = models.IntegerField()
