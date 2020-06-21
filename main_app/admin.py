from django.contrib import admin
from .models import Shoe, Recently_Sold, Store
# Register your models here.

admin.site.register(Shoe)
admin.site.register(Recently_Sold)
admin.site.register(Store)