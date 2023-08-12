from django.urls import path
from .views import Director


urlpatterns = [
    path("", Director.as_view(), name="dashboard"),
]

