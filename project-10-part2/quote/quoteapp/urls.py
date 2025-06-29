from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('quote/', views.quote, name='quote'),
    path('author/', views.author, name='author'),
    path('tag/', views.tag, name='tag'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
]
