from django.forms import ModelForm
from .models import Recently_Sold

class Recently_SoldForm(ModelForm):
  class Meta:
    model = Recently_Sold
    fields = ['date', 'sold_price']