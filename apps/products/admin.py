from django.contrib import admin
from .models import *


class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')


admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Indicator)
admin.site.register(Product)
