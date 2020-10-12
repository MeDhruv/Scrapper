from django.contrib import admin
from app.models import *

# Register your models here.

#admin.site.register(addproduct)
admin.site.register(temp)
admin.site.register(Category)
# admin.site.register(temp)
@admin.register(addproduct)
class addproductAdmin(admin.ModelAdmin):
    list_display=('Product_link','min_price','our_category','Freezed')