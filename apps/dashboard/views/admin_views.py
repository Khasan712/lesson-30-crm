from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.db.models import Q, F, Case, When, OuterRef, FloatField, Subquery, Value
from django.db.models.functions import Coalesce
from apps.dashboard.forms import AddShopWarehouseForm, EditShopForm, ImportProductForm, ProductAddForm
from apps.product.models import Product, Category, ProductSellPrice
from apps.user.models import User
from apps.user.permissions import UserAuthenticateRequiredMixin
from apps.warehouse.models import ImportToWarehouse, ProductInWarehouse, RequestToWarehouse


class Director(UserAuthenticateRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page")

        context = {
            "page": "dashboard" if not page else page
        }
        match page:
            case None | "dashboard":
                context
            
            case 'shops-requests':
                warehouse_id = request.GET.get('warehouse_id')
                warehouse = User.objects.get(id=warehouse_id, role='warehouse')
                shops_requests = RequestToWarehouse.objects.select_related('shop', 'warehouse', 'product').filter(warehouse_id=warehouse_id).annotate(
                    category_title=F("product__category__title"),
                    # warehouse_qty=Case(
                    #     When(
                    #             then=Subquery(
                    #                 RequestToWarehouse.objects.filter(warehouse_id=OuterRef("id"), product_id=OuterRef('product_id')
                    #             )
                                
                    #         )
                    #     )
                    # )
                )
                
                context['shops_requests'] = shops_requests
                context['warehouse'] = warehouse

            case 'shops':
                q = request.GET.get("q")
                from_date = request.GET.get("from_date")
                end_date = request.GET.get("end_date")
                shops = User.objects.filter(role='shop').order_by("-id")
                if q:
                    shops = shops.filter(
                        Q(name__icontains=q) | Q(address__icontains=q) |
                        Q(phone__icontains=q)
                    )
                    context['q'] = q
                if from_date:
                    shops = shops.filter(
                        created_at__gte=from_date
                    )
                if end_date:
                    shops = shops.filter(
                        created_at__lte=end_date
                    )
                context['shops'] = shops
            
            case "shop-detail":
                shop_id = request.GET.get('shop_id')
                shop = User.objects.filter(id=shop_id).first()
                context['shop'] = shop
            
            case "edit-shop":
                shop_id = request.GET.get('shop_id')
                shop = User.objects.filter(id=shop_id).first()
                context['shop'] = shop

            case 'delete-shop':
                shop = request.GET.get("shop_id")
                shop_obj = User.objects.filter(id=shop, role='shop').first()
                shop_obj.delete()
                return HttpResponseRedirect("?page=shops")

            case 'products':
                measure = self.request.GET.get("measure")
                products = Product.objects.order_by('-id')
                if measure:
                    products = products.filter(measure=measure)
                context['products'] = products

            case 'add-product':
                categories = Category.objects.all()
                context['categories'] = categories

            case 'warehouses':
                warehouses = User.objects.filter(role='warehouse').order_by('-id')
                context['warehouses'] = warehouses
            
            case 'warehouse-detail':
                warehouse_id = self.request.GET.get("warehouse_id")
                warehouse = User.objects.filter(role='warehouse', id=warehouse_id).first()
                context['warehouse'] = warehouse

            case 'warehouse-products':
                warehouse_id = self.request.GET.get("warehouse_id")
                warehouse = User.objects.filter(role='warehouse', id=warehouse_id).first()
                warehouse_products = ProductInWarehouse.objects.select_related('warehouse', 'product').filter(
                    warehouse_id=warehouse_id       
                ).order_by("-id")
                context['warehouse_products'] = warehouse_products
                context['warehouse'] = warehouse
            
            case 'import-products-list':
                warehouse_id = self.request.GET.get("warehouse_id")
                warehouse = User.objects.filter(role='warehouse', id=warehouse_id).first()
                import_products = ImportToWarehouse.objects.select_related('warehouse', 'product').filter(
                    warehouse_id=warehouse_id
                ).order_by("-id")
                context['import_products'] = import_products
                context['warehouse'] = warehouse
            
            case 'import-product':
                context['products'] = Product.objects.all()
                context['warehouse_id'] = self.request.GET.get("warehouse_id")

        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        method = request.POST.get("method")
        match method:
            case 'add-shop':
                form = AddShopWarehouseForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.role = 'shop'
                    obj.save()
                    return HttpResponseRedirect("?page=shops")
                else:
                    print(form.errors)
            
            case 'add-product':
                form = ProductAddForm(request.POST)

                price=request.POST.get('price')
                if form.is_valid():
                    obj = form.save()
                    ProductSellPrice.objects.create(
                        product=obj,
                        price=price                       
                          )
                    
                return HttpResponseRedirect("?page=products")

            case 'add-warehouse':
                form = AddShopWarehouseForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.role = 'warehouse'
                    obj.save()
                    return HttpResponseRedirect("?page=warehouses")
                else:
                    print(form.errors)

            
            case 'edit-shop':
                shop_id = request.POST.get("shop_id")
                shop_obj = User.objects.filter(id=shop_id, role='shop').first()
                form = EditShopForm(request.POST, instance=shop_obj)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(f"?page=edit-shop&shop_id={shop_id}")
                else:
                    context = {
                        'page': 'edit-shop',
                        'shop_id': shop_id,
                        'shop': shop_obj,
                        'form': form
                    }
                    return render(request, 'index.html', context)

            case 'import-product':
                warehouse_id = self.request.POST.get('warehouse')
                print(warehouse_id, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                form = ImportProductForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(f"?page=import-products-list&warehouse_id={warehouse_id}")
                else:
                    print(form.errors)
                    context = {
                        'page': 'import-product',
                        'warehouse_id': warehouse_id,
                        'form': form
                    }
                    return render(request, 'index.html', context)
                
        pass

