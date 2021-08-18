from django.contrib.auth.mixins import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import *
from django.shortcuts import redirect
from django.views.generic.edit import *
from .models import *
from .forms import *
from django.db import transaction
from django.http import HttpResponseRedirect
# Create your views here.

class ProductListView(ListView):
    model = Products
    template_name = 'index.html'
    paginate_by = 2

class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/'.format(self.request.user.id)


class Register(CreateView):
    form_class = Registration
    template_name = 'registration.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'

class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    form_class = ProductCreateForm
    success_url = '/'
    template_name = 'create_product.html'
    

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    template_name = 'update_product.html'
    model = Products
    fields = ['name', 'descriptions', 'price', 'quantity']
    success_url = '/'

class ReturnsView(ListView):
    model = Return
    template_name = 'returns.html'

class Returns(CreateView):
    form_class = ReturnsForm
    success_url="/purcase/"
    
    def form_valid(self, form):
        self.purcase = Purcase.objects.get(pk=self.request.POST.get('product_id'))
        self.ret_purcase = form.save(commit=False)
        self.ret_purcase.purcase = self.purcase
        self.ret_purcase.save()
        return super().form_valid(form=form) 

class Confirm(DeleteView):
    model = Purcase
    success_url = reverse_lazy('returns')

    def delete(self, request, success_url=success_url, *args, **kwargs):
        purcase = self.get_object()
        self.product = purcase.product
        self.consumer = purcase.user
        self.consumer.wallet += self.product.price * purcase.quantity
        self.product.quantity += purcase.quantity
        with transaction.atomic():
            self.consumer.save()
            self.product.save()
            purcase.delete() 
        return HttpResponseRedirect(success_url) 

class ReturnDeleteView(LoginRequiredMixin, DeleteView):
    model = Return
    success_url = '/returns/'

class PurcaseView(ListView):
    model = Purcase
    template_name = 'purcase.html'

class ProductAbout(DetailView):
    pk_url_kwarg = "pk"
    model = Products
    template_name = "product.html"
    extra_context = {"form": BuyForm}

class ProductBuy(LoginRequiredMixin, CreateView):
    pk_url_kwarg = "pk"
    login_url = "/login/"
    form_class = BuyForm

    def form_valid(self, form):
        purcase = form.save(commit=False)
        purcase.user = self.request.user
        purcase.product = Products.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form=form)

    def get_success_url(self):
        return "/".format(self.request.user.id)

    def form_invalid(self):
        return redirect(f"/product/about/{self.kwargs['pk']}")


