from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import RecipeViewSet, RecipeCategoryViewSet, RecipeLikeViewSet

app_name = 'recipe' 

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'categories', RecipeCategoryViewSet)
router.register(r'likes', RecipeLikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
