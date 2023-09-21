from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.shortcuts import redirect
from django.http import Http404
from django.http.response import HttpResponse
from apps.user.enums import UserRole

class UserAuthenticateRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("custom_login")

        if self.request.user.role == 'director':
            if request.path != '/':
                return redirect("dashboard")
            return super().dispatch(request, *args, **kwargs)
        
        elif self.request.user.role == 'shop':
            if request.path != '/shop/':
                return redirect("shop")
            return super().dispatch(request, *args, **kwargs)
        
        else:
            raise Http404