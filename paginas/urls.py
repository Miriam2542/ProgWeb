


from django.urls import path
from .views import Inicio, SobreView

urlpatterns = [
 path("", Inicio.as_view(), name = "inicio"),
 path("sobre/", SobreView.as_view(), name = "sobre"),
]
