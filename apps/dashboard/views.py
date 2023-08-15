from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.db.models import Q
from apps.dashboard.forms import AddShopForm, ProductAddForm
from apps.product.models import Product, Category
from apps.user.models import User


class Director(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('custom_login')
        page = request.GET.get("page")

        context = {
            "page": "dashboard" if not page else page
        }
        match page:
            case None | "dashboard":
                context
            
            case 'shops':
                q = request.GET.get("q")
                shops = User.objects.filter(role='shop').order_by("-id")
                if q:
                    shops = shops.filter(
                        Q(name__icontains=q) | Q(address__icontains=q) |
                        Q(phone__icontains=q)
                    )
                    context['q'] = q
                context['shops'] = shops
            
            case "shop-detail":
                shop_id = request.GET.get('shop_id')
                shop = User.objects.filter(id=shop_id)
                context['shop'] = shop

            case 'products':
                products = Product.objects.order_by('-id')
                context.update({
                    'products': products,
                })

            case 'add-product':
                categories = Category.objects.all()
                context['categories'] = categories


        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        method = request.POST.get("method")
        match method:
            case 'add-shop':
                form = AddShopForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("?page=shops")
                else:
                    print(form.errors)
                    print("????")
            
            case 'add-product':
                form = ProductAddForm(request.POST)
                if form.is_valid():
                    form.save()
                return HttpResponseRedirect("?page=products")
        pass

