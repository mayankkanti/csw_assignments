from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:article_id>/share/', views.article_share, name='article_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:article>/', views.article_detail, name='article_detail'),
]
