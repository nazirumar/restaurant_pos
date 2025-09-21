from django.urls import path
from .views import (
    MenuItemListView, MenuItemCreateView, MenuItemDetailView, MenuItemUpdateView, MenuItemDeleteView,
    CategoryListView, AllergenListView, IngredientListView
)

urlpatterns = [
    path('', MenuItemListView.as_view(), name='menu_list'),
    path('create/', MenuItemCreateView.as_view(), name='menu_create'),
    path('<int:pk>/', MenuItemDetailView.as_view(), name='menu_detail'),
    path('<int:pk>/update/', MenuItemUpdateView.as_view(), name='menu_update'),
    path('<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menu_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('allergens/', AllergenListView.as_view(), name='allergen_list'),
    path('ingredients/', IngredientListView.as_view(), name='ingredient_list'),
]