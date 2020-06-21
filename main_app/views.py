from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Shoe, Store, Recently_Sold
from .forms import Recently_SoldForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def shoes_index(request):
    shoes = Shoe.objects.filter(user=request.user)
    return render(request, 'shoes/index.html', {'shoes': shoes})

@login_required
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
    
class ShoeCreate(CreateView, LoginRequiredMixin):
    model = Shoe
    fields = '__all__'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ShoeUpdate(UpdateView, LoginRequiredMixin):
    model = Shoe
    fields = ['brand', 'description', 'year', 'purchased_price', 'image_url']

class ShoeDelete(DeleteView, LoginRequiredMixin):
    model = Shoe
    success_url = '/shoes/'

@login_required    
def assoc_store(request, shoe_id, store_id):
    shoe = Shoe.objects.get(id=shoe_id)
    shoe.stores.add(store_id)
    return redirect('detail', shoe_id=shoe_id)

@login_required
def unassoc_store(request, shoe_id, store_id):
  Shoe.objects.get(id=shoe_id).stores.remove(store_id)
  return redirect('detail', shoe_id=shoe_id)

@login_required
def add_recently_sold(request, shoe_id):
    form = Recently_SoldForm(request.POST)
    if form.is_valid():
        new_recently_sold = form.save(commit=False)
        new_recently_sold.shoe_id = shoe_id
        new_recently_sold.save()
    return redirect('detail', shoe_id=shoe_id)

class StoreList(ListView, LoginRequiredMixin):
    model = Store

class StoreDetail(DetailView, LoginRequiredMixin):
    model = Store

class StoreCreate(CreateView, LoginRequiredMixin):
    model = Store
    fields = '__all__'
    
class StoreUpdate(UpdateView, LoginRequiredMixin):
    model = Store
    fields = ['name', 'url']
    
class StoreDelete(DeleteView, LoginRequiredMixin):
    model = Storesuccess_url = '/stores/'
    
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      #This is how we programmatically login
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again!'
  # A bad POST or it's a GET
  form = UserCreationForm()
  context = {
    'form': form,
    'error_message': error_message
  }
  return render(request, 'registration/signup.html', context)
