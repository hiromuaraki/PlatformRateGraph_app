from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:cnt>', views.index, name='index')
]