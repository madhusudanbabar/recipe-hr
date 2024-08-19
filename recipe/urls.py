from django.urls import path
from recipe import views

app_name = 'recipe'

urlpatterns = [
    path('', views.RecipeListAPIView.as_view(), name="recipe-list"),
    path('<int:pk>/', views.RecipeAPIView.as_view(), name="recipe-detail"),
    path('create/', views.RecipeCreateAPIView.as_view(), name="recipe-create"),
    path('<int:pk>/like/', views.RecipeLikeAPIView.as_view(),
         name='recipe-like'),
    path('test-celery/', views.test_celery, name='test_celery'),
    path('test-celery/long/', views.start_long_running_task, name='test_long_task'),
]
