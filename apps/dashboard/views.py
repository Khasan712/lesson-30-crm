from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect

from apps.dashboard.forms import AddShopForm
from apps.user.models import User


class Director(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('custom_login')
        page = request.GET.get("page")

        context = {
            "page": "dashboard"
        }
        match page:
            case None | "dashboard":
                context
            
            case 'shops':
                shops = User.objects.filter(role='shop').order_by("-id")
                context['page'] = 'shops'
                context['shops'] = shops

            case "add-shop":
                context['page'] = 'add-shop'

        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        method = request.POST.get("method")
        match method:
            case 'add-shop':
                print("Kirdi")
                form = AddShopForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("?page=shops")
                else:
                    print(form.errors)
        pass

