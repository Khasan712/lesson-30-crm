from django.shortcuts import render,redirect
from django.views  import View
from django.http import HttpResponseRedirect
from apps.dashboard.forms import AddShopWarehouseForm, EditshopForm, ProductAddForm, EditProductForm, EditWarehouseForm, ImportProductForm
from apps.user.models import User
from apps.product.models import Product, Category, ProductSellPrice, ShopProduct
from apps.user.permissions import UserAuthenticateRequiredMixin
from apps.warehouse.models import ProductInWarehouse, ImportToWerhouse, RequestToWarehouse
from django.db.models import Q, F

class Director(UserAuthenticateRequiredMixin, View):
    
    
    
    def get(self, request, *args, **kwargs):
        page=request.GET.get("page")

        context = {
            "page" : "dashboard" if not page  else page
        }
        match page:
            case None | "dashboard":
                context

            case 'shops':
                q=request.GET.get("q")
                from_date=request.GET.get("from_date")
                end_date=request.GET.get("end_date")
                shops=User.objects.filter(role="shop").order_by("-id")
                if q:
                    shops=shops.filter(Q(name__icontains=q) |
                                       Q(address__icontains=q))
                
                if from_date:
                    shops=shops.filter(
                        created_at__gte=from_date
                    )
                if end_date:
                    shops=shops.filter(
                        created_at__lte=end_date
                    )
                context['shops'] = shops
                
                
            case "product":
                measure=request.GET.get('measure')
                
                products=Product.objects.order_by("-id")
                
                if measure:
                    products=products.filter(measure=measure)
                context.update({
                    'products' : products,
                    'page' : page,
                   
                })
            
                
            case "add-shop":
                # shop_id=request.GET.get('shop_id')
                # shop=User.objects.filter(id=shop, role='shop').first()
                context['page'] = 'add-shop'
                
            case 'shop-delete':
                shop=request.GET.get("shop_id")
                shop_obj=User.objects.filter(id=shop, role='shop').first()
                shop_obj.delete()
                return HttpResponseRedirect("?page=shops")
            
            case 'edit-shop':
                shop_id=request.GET.get('shop_id')
                shop=User.objects.filter(id=shop_id, role='shop').first()
                context['shop'] = shop
            
        
            case "shop-detail":
                shop_id=request.GET.get('shop_id')
                shop = User.objects.filter(id=shop_id)
                context["page"] = 'shop-detail'
                context['shop'] = shop

            
            case "add-product":
                categories=Category.objects.all()
                context['categories'] = categories
                context['page'] = page
                
            case "product-delete":
                product=request.GET.get('product_id')
                product_obj=Product.objects.filter(id=product).first()
                product_obj.delete()
                return HttpResponseRedirect("?page=product")
            
            case "edit-product":
                product_id=request.GET.get('product_id')
                product=Product.objects.filter(id=product_id).first()
                categories=Category.objects.all()
                context.update({
                    'products' : product,
                    'page' : page,
                    'categories': categories
                })
                
                
            case "warehouses":
                warehouses=User.objects.filter(role='warehouse').order_by('-id')
                context['warehouses'] = warehouses
                
            case "add-warehouse":
                warehouses=User.objects.filter(role='warehouse').order_by('-id')
                context['warehouses'] = warehouses
                
            case "warehouse-delete":
                warehouse=request.GET.get('warehouse_id')
                warehouse_obj=User.objects.filter(id=warehouse, role='warehouse').first()
                warehouse_obj.delete()
                return HttpResponseRedirect("?page=warehouses")
            
            
            case 'edit-warehouse':
                warehouse_id=request.GET.get('warehouse_id')
                warehouse_ob=User.objects.filter(id=warehouse_id, role='warehouse').first()
                context['warehouses'] = warehouse_ob
                
             
            case 'warehouse-products':
                warehouse_id=self.request.GET.get('warehouse_id')
                warehouse=User.objects.filter(role='warehouse', id=warehouse_id).first()
                warehouse_products=ProductInWarehouse.objects.select_related('warehouse', 'product').filter(
                    warehouse_id=warehouse_id
                ).order_by("-id")
                context['warehouse_products']= warehouse_products
                context['warehouse'] = warehouse
                
                
            case 'import-products-list':
                # price=request.GET.get('price')
                warehouse_id=request.GET.get('warehouse_id')
                warehouse=User.objects.filter(role='warehouse', id=warehouse_id).first()
                import_products=ImportToWerhouse.objects.select_related('warehouse', 'product').filter(
                    warehouse_id=warehouse_id
                    # price=price
                ).order_by("-id")
                context['import_products']= import_products
                context['warehouse'] = warehouse
                
                
            case 'import-product':
                context['products'] = Product.objects.all()
                context['warehouse_id'] = request.GET.get('warehouse_id')
                
                
            
            case 'shops-requests':
                warehouse_id=request.GET.get('warehouse_id')
                warehouse=User.objects.get(id=warehouse_id, role='warehouse')
                shops_requests=RequestToWarehouse.objects.select_related("shop", "warehouse", "product").filter(
                    warehouse_id=warehouse_id
                ).annotate(category_title=F("product__category__title"))
                
                context["shops_requests"]=shops_requests  
                context["warehouse"]=warehouse  
                
                
            case 'warehouse-new-request':
                warehouse_request_id=request.GET.get("warehouse_request_id")
                obj=RequestToWarehouse.objects.filter(
                    id=warehouse_request_id, status='new'
                ).first()
                if obj:
                    context['warehouse_new_obj'] = obj
                else :
                    return redirect("shops-requests")
            
                       
                
                                
        return render(request, 'index.html', context)
         




    def post(self, request, *args, **kwargs):
        method= request.POST.get("method")
        match method:
            case 'add-shop':
                print(request.POST)
                form=AddShopWarehouseForm(request.POST)
                if form.is_valid():
                    obj = form.save()
                    obj.role = 'shop'
                    obj.save()
                    return HttpResponseRedirect('?page=shop')
                else:
                    print(form.errors)
                    
            case 'add-product':
                price=request.POST.get('price')
                form=ProductAddForm(request.POST)
                if form.is_valid():
                    obj=form.save()
                    ProductSellPrice.objects.create(
                        product=obj,
                        price=price
                    )
                    return HttpResponseRedirect('?page=product')
                else:
                    print(form.errors)
            
            case'add-warehouse':
                form=AddShopWarehouseForm(request.POST)
                if form.is_valid():
                    obj=form.save()
                    obj.role='warehouse'
                    obj.save()
                    return HttpResponseRedirect("?page=warehouses")
                else :
                    print(form.errors, '?????????????????????????????')
                
            case 'edit-shop':
                shop_id=request.POST.get('shop_id')
                shop_obj=User.objects.filter(id=shop_id, role='shop').first()
                form=EditshopForm(request.POST, instance=shop_obj)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(f"?page='edit-shop'&shop_id={shop_id}")
                else:
                    print(form.errors)
        
            case 'edit-product':
                product_id=request.POST.get('product_id')
                price=request.POST.get('price')
                product=Product.objects.filter(id=product_id).first()
                form=EditProductForm(request.POST, instance=product)
                if form.is_valid():
                    obj=form.save()
                    ProductSellPrice.objects.create(
                        product=obj,
                        price=price
                    )
                    return HttpResponseRedirect('?page=product')
                else:
                    print("===========================================================")
                    print(form.errors)
                    print("===========================================================")
                    
            case 'edit-warehouse':
                warehouse_id=request.POST.get('warehouse_id')
                warehouse_ob=User.objects.filter(id=warehouse_id, role='warehouse').first()
                form=EditWarehouseForm(request.POST, instance=warehouse_ob)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('?page=warehouses')
                else:
                    print(form.errors)
                
                
                
            case 'import-product':
                price=request.POST.get('price')
                warehouse_id=request.POST.get('warehouse')
                form = ImportProductForm(request.POST)
                if form.is_valid():
                    form.save()
                    # ProductSellPrice.objects.create(
                    #     product=obj.product,
                    #     price=price
                    # )
                    return HttpResponseRedirect(f"?page=import-products-list&warehouse_id={warehouse_id}")
                else:
                    context = {
                        'page' : 'import-product',
                        'warehouse_id' : warehouse_id,
                        'form' : form
                    }
                    return render(request, 'index.html', context)
                
                
            case  'warehouse-new-request':
                    page = request.POST.get('page')
                    request_warehouse_id=request.POST.get("obj")
                    request_warehouse=RequestToWarehouse.objects.filter(
                        id=request_warehouse_id, status="new",  shop_id=request.user.id
                    ).first()
                    
                    if not request_warehouse:
                        return HttpResponseRedirect(f"?page={method}&request_warehouse_id={request_warehouse_id}")
                    request_warehouse.status = "confirmed"
                    shop_product, _ =ShopProduct.objects.get_or_create(
                        shop_id=request.user.id,
                        product_id=request_warehouse.product.id)
                    
                    shop_product.qty += request_warehouse.qty
                    request_warehouse.save()
                    shop_product.save()
                    return HttpResponseRedirect(F"?page={page}")
                
                    
                    