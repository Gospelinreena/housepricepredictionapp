from django.urls import path
from . import views

urlpatterns = [
    path('', views.descriptive),
    path('descriptive/', views.descriptive),
    path('inferential/', views.inferential),
    path('prediction/', views.prediction),
    path('predict/', views.predict),
]