from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.shortcuts import redirect
from django.http import Http404
from django.http.response import HttpResponseRedirect
from apps.user.enoms import UserRole



class UserAuthenticateRequiredMixin(AccessMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('custom_login')
        
        if self.request.user.role == 'director':
            print(request.path)
            if request.path != "/":
                raise Http404
            return super().dispatch(request, *args, **kwargs)
        
        if self.request.user.role == 'shop':
            if request.path != '/shop/':
                # raise Http404
                return redirect("shop")
            return super().dispatch(request, *args, **kwargs)
        
        else:
            raise Http404
                