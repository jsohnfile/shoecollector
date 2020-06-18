from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Shoe, Recently_Sold
from .forms import Recently_SoldForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def shoes_index(request):
    shoes = Shoe.objects.all()
    return render(request, 'shoes/index.html', {'shoes': shoes})

def shoes_detail(request, shoe_id):
    shoe = Shoe.objects.get(id=shoe_id)
    sold = Recently_Sold.objects.filter(shoe=shoe_id)
    print(sold)
    recently_sold_form = Recently_SoldForm()
    return render(request, 'shoes/detail.html', {
        'shoe': shoe,
        'recently_sold_form': recently_sold_form,
        'sold': sold
        })


class ShoeCreate(CreateView):
    model = Shoe
    fields = '__all__'
    
class ShoeUpdate(UpdateView):
    model = Shoe
    fields = ['brand', 'description', 'year', 'purchased_price', 'image_url']

class ShoeDelete(DeleteView):
    model = Shoe
    success_url = '/shoes/'
    
def add_recently_sold(request, shoe_id):
    form = Recently_SoldForm(request.POST)
    if form.is_valid():
        new_recently_sold = form.save(commit=False)
        new_recently_sold.shoe_id = shoe_id
        new_recently_sold.save()
    return redirect('detail', shoe_id=shoe_id)