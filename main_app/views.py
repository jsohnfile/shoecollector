from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Shoe, Store, Recently_Sold
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
    stores_shoe_isnt_available = Store.objects.exclude(id__in = shoe.stores.all().values_list('id'))
    recently_sold_form = Recently_SoldForm()
    urlshoe = shoe.name.replace(' ', '-')
    return render(request, 'shoes/detail.html', {
        'shoe': shoe,
        'recently_sold_form': recently_sold_form,
        'stores': stores_shoe_isnt_available,
        'urlshoe': urlshoe
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
    
def assoc_store(request, shoe_id, store_id):
    shoe = Shoe.objects.get(id=shoe_id)
    shoe.stores.add(store_id)
    return redirect('detail', shoe_id=shoe_id)

def add_recently_sold(request, shoe_id):
    form = Recently_SoldForm(request.POST)
    if form.is_valid():
        new_recently_sold = form.save(commit=False)
        new_recently_sold.shoe_id = shoe_id
        new_recently_sold.save()
    return redirect('detail', shoe_id=shoe_id)

class StoreList(ListView):
    model = Store

class StoreDetail(DetailView):
    model = Store

class StoreCreate(CreateView):
    model = Store
    fields = '__all__'
    
class StoreUpdate(UpdateView):
    model = Store
    fields = ['name', 'url']
    
class StoreDelete(DeleteView):
    model = Storesuccess_url = '/stores/'
