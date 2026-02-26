from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Product

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = ['name', 'link', 'description', 'creation_date', 'version', 'project_ref', 'tech_stack']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')
    success_message = "Product '%(name)s' was recorded successfully."

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = ['name', 'link', 'description', 'creation_date', 'version', 'project_ref', 'tech_stack']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')
    success_message = "Product '%(name)s' was updated successfully."

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f"Product '{obj.name}' was removed.")
        return super().delete(request, *args, **kwargs)
