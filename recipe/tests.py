from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser
from .models import Recipe, RecipeCategory, RecipeLike
from django.core.files.uploadedfile import SimpleUploadedFile

class RecipeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = RecipeCategory.objects.create(name='Test Category')

        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            desc='Test Description',
            cook_time='01:00:00',
            ingredients='Test Ingredients',
            procedure='Test Procedure',
            category=self.category,
            author=self.user
        )

    def test_recipe_list(self):
        response = self.client.get(reverse('recipe:recipe-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_recipe_update(self):
        recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            picture=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            title='Old Title',
            desc='Old Description',
            cook_time='01:00:00',
            ingredients='Old Ingredients',
            procedure='Old Procedure'
        )
        data = {
            'title': 'Updated Recipe',
            'desc': 'Updated Description',
            'cook_time': '03:00:00',
            'ingredients': 'Updated Ingredients',
            'procedure': 'Updated Procedure',
            'category': {'id': self.category.id, 'name': self.category.name}, 
            'picture': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        }
        url = reverse('recipe:recipe-detail', args=[recipe.id])  
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_recipe_delete(self):
        url = reverse('recipe:recipe-detail', args=[self.recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_recipe_like_create(self):
        data = {
            'recipe': self.recipe.id
        }
        response = self.client.post(reverse('recipe:recipelike-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_recipe_like_delete(self):
        like = RecipeLike.objects.create(user=self.user, recipe=self.recipe)
        url = reverse('recipe:recipelike-detail', args=[like.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
