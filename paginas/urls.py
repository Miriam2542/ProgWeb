
from django.urls import path
from .views import Inicio, SobreView
from. views import CampusCreate

urlpatterns = [
 path("", Inicio.as_view(), name = "inicio"),
 path("sobre/", SobreView.as_view(), name = "sobre"),

 path("adicionar/categoria", CampusCreate.as_view()),
]
