from django.db import models


class CompanyDataset(models.Model):
    data_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    year_founded = models.IntegerField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    size_range = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    current_employee_estimate = models.IntegerField(blank=True, null=True)
    total_employee_estimate = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
