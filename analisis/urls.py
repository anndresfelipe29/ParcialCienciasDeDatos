from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    # ex: /polls/p
    path('p', views.prueba, name='detail'),
    # ex: /polls/5/
   # path('<int:question_id>/', views.prueba, name='prueba'),
   path('imagen', views.imagen, name='imagen'),
   path('analisis/<int:eleccion>/', views.analisis, name='analisis'),
   
]