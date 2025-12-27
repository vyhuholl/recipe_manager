from django.contrib import admin
from .models import Recipe, Ingredient, Tag


class IngredientInline(admin.TabularInline):
    """Inline admin for ingredients."""
    model = Ingredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin interface for Recipe model."""
    list_display = ['name', 'servings', 'prep_time', 'cook_time', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    inlines = [IngredientInline]
    filter_horizontal = ['tags']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model."""
    list_display = ['name', 'recipe_count']
    search_fields = ['name']

    def recipe_count(self, obj):
        """Return the number of recipes with this tag."""
        return obj.recipes.count()
    recipe_count.short_description = 'Recipes'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Admin interface for Ingredient model."""
    list_display = ['name', 'quantity', 'unit', 'recipe']
    list_filter = ['recipe']
    search_fields = ['name', 'recipe__name']

