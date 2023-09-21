from ipaddress import summarize_address_range
from django.shortcuts import render, redirect
from django.views import View
from apps.dashboard.forms import RequestToWarehouseForm, TradeForm
from apps.product.models import Product, ProductSellPrice, ShopProduct, Trade
from apps.user.models import User
from apps.user.permissions import UserAuthenticateRequiredMixin
from apps.warehouse.models import RequestToWarehouse
from django.http.response import HttpResponseRedirect
from django.db.models import F, Subquery, OuterRef, FloatField, Sum, Case, When, IntegerField, Q, Count
from django.db.models.functions import Coalesce
import datetime


class Shop(UserAuthenticateRequiredMixin, View):

    def get_filter_date(self):
        date_start = self.request.GET.get("date_start")
        date_end = self.request.GET.get("date_end")
        days = self.request.GET.get("days")
        today = datetime.datetime.today()

        if days or not days and not date_start and not date_end:
            days = 31 if not days else days
            date_start = today - datetime.timedelta(days=int(days))
            date_end = datetime.datetime.now()
            days = (
                datetime.datetime.strptime(date_end.strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.datetime.strptime(date_start.strftime('%Y-%m-%d'), '%Y-%m-%d')
            ).days
            return {
                "date_start": date_start,
                "date_end": date_end,
                "day": days
            }

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page")
        error = kwargs.get("error")
        context = {
            "page": "dashboard" if not page else page,
            'error': error
        }
        match page:
            case None | "dashboard":
                print(self.get_filter_date()['day'])
                products_statistics = ShopProduct.objects.select_related('product', 'shop').filter(
                    shop_id=request.user.id
                ).annotate(
                    sold_qty=Subquery(
                        Trade.objects.filter(
                            shop_id=OuterRef("shop_id"), product_id=OuterRef("product_id"),
                            created_at__gte=self.get_filter_date()['date_start'], created_at__lte=self.get_filter_date()['date_end']
                        ).values("product_id").annotate(t=Sum("qty")).values("t")[:1], output_field=IntegerField()
                    ),
                    sold_price=Subquery(
                        Trade.objects.filter(
                            shop_id=OuterRef("shop_id"), product_id=OuterRef("product_id"),
                            created_at__gte=self.get_filter_date()['date_start'], created_at__lte=self.get_filter_date()['date_end']
                        ).values("product_id").annotate(t=Sum(F("sold_price") * F("qty"))).values("t")[:1]
                    ),
                    total_price=Subquery(
                        Trade.objects.filter(
                            shop_id=OuterRef("shop_id"), product_id=OuterRef("product_id"),
                            created_at__gte=self.get_filter_date()['date_start'], created_at__lte=self.get_filter_date()['date_end']
                        ).values("product_id").annotate(t=Sum("sold_price")).values("t")[:1]
                    ),
                    trade_qty=Subquery(
                        Trade.objects.filter(
                            shop_id=OuterRef("shop_id"), product_id=OuterRef("product_id"),
                            created_at__gte=self.get_filter_date()['date_start'], created_at__lte=self.get_filter_date()['date_end']
                        ).values("product_id").annotate(t=Count(F("sold_price") * F("qty"))).values("t")[:1]
                    ),
                    daily_trade=F("sold_qty") / self.get_filter_date()['day'],
                    everage_price=F("sold_price") / self.get_filter_date()['day'],
                    daily_price=F("total_price") / F("trade_qty"),
                    category=F("product__category__title")
                )
                context['products_statistics'] = products_statistics

            case "trade":
                trads = Trade.objects.filter(
                    shop_id=request.user.id
                ).annotate(
                    category_title=F("product__category__title"), product_title=F("product__title"),
                ).values("id", 'product_title', 'category_title', 'sold_price', 'qty', 'created_at').order_by("-id")[:10]

                products = ShopProduct.objects.select_related('product').annotate(
                    product_price=Subquery(ProductSellPrice.objects.filter(product_id=OuterRef("product_id")).values('price')[:1])
                )
                context.update({
                    'products': products,
                    'trads': trads
                })
            
            case "request-to-warehouse-list":
                status = request.GET.get('status')
                history_requests = RequestToWarehouse.objects.select_related(
                    "shop", "warehouse", "product"    
                ).filter(shop_id=request.user.id).annotate(
                    category_name=F("product__category__title")
                )
                if status and status in ['new', 'accepted', 'rejected', 'confirmed']:
                    history_requests = history_requests.filter(status=status)
                context.update({
                    'history_requests': history_requests
                })
            
            case "request-to-warehouse":
                warehouses = User.objects.filter(role='warehouse').order_by("-id")
                products = Product.objects.all()
                context.update({
                    "warehouses": warehouses,
                    "products": products,
                })

            case 'products':
                products = ShopProduct.objects.select_related("product", "shop").filter(
                    shop_id=request.user.id
                )
                context['products'] = products

            case 'confirm-request':
                reqeust_to_warehouse_id = request.GET.get("request_warehouse_id")
                request_warehouse_obj = RequestToWarehouse.objects.filter(id=reqeust_to_warehouse_id, status='accepted').first()
                if request_warehouse_obj:
                    context['request_warehouse'] = request_warehouse_obj
                else:
                    return redirect("shop")
            
        return render(request, 'shop_index.html', context)
    
    def post(self, request, *args, **kwargs):
        method = request.POST.get("method")
        page = request.POST.get("page")

        match method:
            case 'trade':
                product = request.POST['product']
                qty = request.POST['qty']
                product_in_shop = ShopProduct.objects.get(product_id=product)
                if int(qty) > product_in_shop.qty:
                    error = "Maxsulot omborda yetarli emas."
                    return self.get(request, error=error)
                
                form = TradeForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    if request.POST.get("price"):
                        obj.sold_price = request.POST.get("price")
                    else:
                        obj.sold_price = obj.product.price.price
                    obj.shop = request.user
                    obj.save()
                    product_in_shop.qty-=int(qty)
                    product_in_shop.save()
                    return self.get(request)
                else:
                    context = {
                        'page': page,
                        'form': form
                    }
                    return render(request, "shop_index.html", context)
                
            case "request-to-warehouse":
                form = RequestToWarehouseForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.shop = request.user
                    obj.save()
                    return HttpResponseRedirect(f"?page={page}")
                else:
                    context = {
                        'page': method,
                        'form': form    
                    }
                    return render(request, "shop_index.html", context)  

            case "confirm-request":
                page = request.POST.get("page")
                request_warehouse_id = request.POST.get("obj")
                request_warehouse = RequestToWarehouse.objects.filter(
                    id=request_warehouse_id, status="accepted", shop_id=request.user.id
                ).first()
                if not request_warehouse:
                    return HttpResponseRedirect(f"?page={method}&request_warehouse_id={request_warehouse_id}")
                request_warehouse.status="confirmed"
                shop_product, _ = ShopProduct.objects.get_or_create(
                    shop_id=request.user.id,
                    product_id=request_warehouse.product.id
                )
                shop_product.qty+=request_warehouse.qty
                request_warehouse.save()
                shop_product.save()
                return HttpResponseRedirect(f"?page={page}")
