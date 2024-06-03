from django.contrib import admin

# Register your models here.
from count_app.models import CompanyDataset


class CompanyDatasetAdmin(admin.ModelAdmin):
    pass


admin.site.register(CompanyDataset, CompanyDatasetAdmin)
