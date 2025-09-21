from django.contrib import admin
from .models import Category, Allergen, Ingredient, MenuItem, MenuItemIngredient


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant')
    list_filter = ('tenant',)
    search_fields = ('name',)
    ordering = ('tenant', 'name')
    autocomplete_fields = ('tenant',)


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'unit')
    list_filter = ('tenant',)
    search_fields = ('name',)
    ordering = ('tenant', 'name')
    autocomplete_fields = ('tenant',)


class MenuItemIngredientInline(admin.TabularInline):
    model = MenuItemIngredient
    extra = 1
    autocomplete_fields = ('ingredient',)
    min_num = 0


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'category', 'price')
    list_filter = ('tenant', 'category')
    search_fields = ('name',)
    ordering = ('tenant', 'name')
    autocomplete_fields = ('tenant', 'category', 'ingredients', 'allergens')
    filter_horizontal = ('allergens',)
    inlines = [MenuItemIngredientInline]


@admin.register(MenuItemIngredient)
class MenuItemIngredientAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'ingredient', 'quantity')
    list_filter = ('menu_item__tenant',)
    search_fields = ('menu_item__name', 'ingredient__name')
    autocomplete_fields = ('menu_item', 'ingredient')
