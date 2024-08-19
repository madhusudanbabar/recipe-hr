from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Recipe, RecipeCategory, RecipeLike
from .serializers import RecipeSerializer, RecipeCategorySerializer, RecipeLikeSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-created_at')
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeCategoryViewSet(viewsets.ModelViewSet):
    queryset = RecipeCategory.objects.all()
    serializer_class = RecipeCategorySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class RecipeLikeViewSet(viewsets.ModelViewSet):
    queryset = RecipeLike.objects.all()
    serializer_class = RecipeLikeSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
