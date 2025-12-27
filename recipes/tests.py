from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Recipe, Ingredient, Tag


class RecipeModelTest(TestCase):
    """Test cases for Recipe model."""

    def test_create_recipe_with_required_fields(self):
        """Test creating a recipe with only required fields."""
        recipe = Recipe.objects.create(
            name="Chocolate Chip Cookies",
            instructions="Mix ingredients and bake"
        )
        self.assertEqual(recipe.name, "Chocolate Chip Cookies")
        self.assertEqual(recipe.instructions, "Mix ingredients and bake")
        self.assertIsNotNone(recipe.created_at)
        self.assertIsNotNone(recipe.updated_at)

    def test_create_recipe_with_all_fields(self):
        """Test creating a recipe with all fields."""
        recipe = Recipe.objects.create(
            name="Chocolate Chip Cookies",
            description="Delicious homemade cookies",
            servings=24,
            prep_time=15,
            cook_time=12,
            instructions="Mix ingredients and bake at 350F"
        )
        self.assertEqual(recipe.name, "Chocolate Chip Cookies")
        self.assertEqual(recipe.description, "Delicious homemade cookies")
        self.assertEqual(recipe.servings, 24)
        self.assertEqual(recipe.prep_time, 15)
        self.assertEqual(recipe.cook_time, 12)
        self.assertEqual(recipe.instructions, "Mix ingredients and bake at 350F")

    def test_recipe_requires_name(self):
        """Test that recipe name is required."""
        with self.assertRaises(ValidationError):
            recipe = Recipe(name="", instructions="Some instructions")
            recipe.full_clean()

    def test_recipe_requires_instructions(self):
        """Test that recipe instructions are required."""
        with self.assertRaises(ValidationError):
            recipe = Recipe(name="Test Recipe", instructions="")
            recipe.full_clean()

    def test_recipe_str_representation(self):
        """Test recipe string representation."""
        recipe = Recipe.objects.create(
            name="Test Recipe",
            instructions="Test instructions"
        )
        self.assertEqual(str(recipe), "Test Recipe")

    def test_recipe_ordering(self):
        """Test that recipes are ordered by creation date (newest first)."""
        recipe1 = Recipe.objects.create(
            name="First Recipe",
            instructions="Instructions 1"
        )
        recipe2 = Recipe.objects.create(
            name="Second Recipe",
            instructions="Instructions 2"
        )
        recipes = list(Recipe.objects.all())
        self.assertEqual(recipes[0], recipe2)
        self.assertEqual(recipes[1], recipe1)

    def test_recipe_update_modifies_updated_at(self):
        """Test that updating a recipe updates the updated_at timestamp."""
        recipe = Recipe.objects.create(
            name="Original Name",
            instructions="Original instructions"
        )
        original_updated = recipe.updated_at
        recipe.name = "Updated Name"
        recipe.save()
        recipe.refresh_from_db()
        self.assertGreater(recipe.updated_at, original_updated)


class IngredientModelTest(TestCase):
    """Test cases for Ingredient model."""

    def setUp(self):
        """Set up test recipe."""
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            instructions="Test instructions"
        )

    def test_create_ingredient_with_all_fields(self):
        """Test creating an ingredient with all fields."""
        ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            quantity=2.5,
            unit="cups",
            name="flour"
        )
        self.assertEqual(ingredient.recipe, self.recipe)
        self.assertEqual(ingredient.quantity, 2.5)
        self.assertEqual(ingredient.unit, "cups")
        self.assertEqual(ingredient.name, "flour")

    def test_create_ingredient_without_quantity_and_unit(self):
        """Test creating an ingredient with only name."""
        ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            name="salt"
        )
        self.assertEqual(ingredient.name, "salt")
        self.assertIsNone(ingredient.quantity)
        self.assertEqual(ingredient.unit, "")

    def test_ingredient_requires_name(self):
        """Test that ingredient name is required."""
        with self.assertRaises(ValidationError):
            ingredient = Ingredient(recipe=self.recipe, name="")
            ingredient.full_clean()

    def test_ingredient_requires_recipe(self):
        """Test that ingredient requires a recipe."""
        ingredient = Ingredient(name="flour")
        with self.assertRaises(IntegrityError):
            ingredient.save()

    def test_ingredient_str_with_all_fields(self):
        """Test ingredient string representation with all fields."""
        ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            quantity=2.5,
            unit="cups",
            name="flour"
        )
        self.assertEqual(str(ingredient), "2.5 cups flour")

    def test_ingredient_str_with_quantity_only(self):
        """Test ingredient string representation with quantity only."""
        ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            quantity=3,
            name="eggs"
        )
        self.assertEqual(str(ingredient), "3 eggs")

    def test_ingredient_str_with_name_only(self):
        """Test ingredient string representation with name only."""
        ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            name="salt"
        )
        self.assertEqual(str(ingredient), "salt")

    def test_ingredient_cascade_delete(self):
        """Test that ingredients are deleted when recipe is deleted."""
        ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            name="flour"
        )
        ingredient_id = ingredient.id
        self.recipe.delete()
        self.assertFalse(Ingredient.objects.filter(id=ingredient_id).exists())


class TagModelTest(TestCase):
    """Test cases for Tag model."""

    def test_create_tag(self):
        """Test creating a tag."""
        tag = Tag.objects.create(name="dessert")
        self.assertEqual(tag.name, "dessert")

    def test_tag_name_is_unique(self):
        """Test that tag names must be unique."""
        Tag.objects.create(name="dessert")
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name="dessert")

    def test_tag_str_representation(self):
        """Test tag string representation."""
        tag = Tag.objects.create(name="vegetarian")
        self.assertEqual(str(tag), "vegetarian")

    def test_tag_ordering(self):
        """Test that tags are ordered by name."""
        tag2 = Tag.objects.create(name="zebra")
        tag1 = Tag.objects.create(name="apple")
        tags = list(Tag.objects.all())
        self.assertEqual(tags[0], tag1)
        self.assertEqual(tags[1], tag2)


class RecipeTagRelationshipTest(TestCase):
    """Test cases for Recipe-Tag many-to-many relationship."""

    def setUp(self):
        """Set up test data."""
        self.recipe = Recipe.objects.create(
            name="Chocolate Cake",
            instructions="Bake a cake"
        )
        self.tag1 = Tag.objects.create(name="dessert")
        self.tag2 = Tag.objects.create(name="vegetarian")

    def test_add_tags_to_recipe(self):
        """Test adding tags to a recipe."""
        self.recipe.tags.add(self.tag1, self.tag2)
        self.assertEqual(self.recipe.tags.count(), 2)
        self.assertIn(self.tag1, self.recipe.tags.all())
        self.assertIn(self.tag2, self.recipe.tags.all())

    def test_remove_tag_from_recipe(self):
        """Test removing a tag from a recipe."""
        self.recipe.tags.add(self.tag1, self.tag2)
        self.recipe.tags.remove(self.tag1)
        self.assertEqual(self.recipe.tags.count(), 1)
        self.assertNotIn(self.tag1, self.recipe.tags.all())
        self.assertIn(self.tag2, self.recipe.tags.all())

    def test_tag_reuses_existing_tag(self):
        """Test that creating a tag with existing name reuses the tag."""
        # Use get_or_create to demonstrate tag reuse
        tag1, created = Tag.objects.get_or_create(name="baking")
        self.assertTrue(created)  # First time, tag is created
        recipe1 = Recipe.objects.create(
            name="Recipe 1",
            instructions="Instructions 1"
        )
        recipe2 = Recipe.objects.create(
            name="Recipe 2",
            instructions="Instructions 2"
        )
        recipe1.tags.add(tag1)
        recipe2.tags.add(tag1)
        # Try to get or create the same tag again
        tag2, created = Tag.objects.get_or_create(name="baking")
        self.assertFalse(created)  # Second time, existing tag is reused
        self.assertEqual(tag1.id, tag2.id)  # Same tag object
        self.assertEqual(Tag.objects.filter(name="baking").count(), 1)
        self.assertEqual(tag1.recipes.count(), 2)

    def test_tag_remains_after_recipe_deletion(self):
        """Test that tags remain after recipe deletion."""
        self.recipe.tags.add(self.tag1)
        tag_id = self.tag1.id
        self.recipe.delete()
        self.assertTrue(Tag.objects.filter(id=tag_id).exists())

    def test_filter_recipes_by_tag(self):
        """Test filtering recipes by tag."""
        recipe1 = Recipe.objects.create(
            name="Cake",
            instructions="Bake"
        )
        recipe2 = Recipe.objects.create(
            name="Salad",
            instructions="Mix"
        )
        recipe1.tags.add(self.tag1)
        recipe2.tags.add(self.tag2)
        dessert_recipes = Recipe.objects.filter(tags=self.tag1)
        self.assertEqual(dessert_recipes.count(), 1)
        self.assertEqual(dessert_recipes.first(), recipe1)


class RecipeIngredientRelationshipTest(TestCase):
    """Test cases for Recipe-Ingredient relationship."""

    def setUp(self):
        """Set up test data."""
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            instructions="Test instructions"
        )

    def test_add_ingredients_to_recipe(self):
        """Test adding multiple ingredients to a recipe."""
        ingredient1 = Ingredient.objects.create(
            recipe=self.recipe,
            quantity=2,
            unit="cups",
            name="flour"
        )
        ingredient2 = Ingredient.objects.create(
            recipe=self.recipe,
            quantity=1,
            unit="cup",
            name="sugar"
        )
        self.assertEqual(self.recipe.ingredients.count(), 2)
        self.assertIn(ingredient1, self.recipe.ingredients.all())
        self.assertIn(ingredient2, self.recipe.ingredients.all())

    def test_retrieve_recipe_with_ingredients(self):
        """Test retrieving a recipe with its ingredients."""
        Ingredient.objects.create(
            recipe=self.recipe,
            quantity=2,
            unit="cups",
            name="flour"
        )
        Ingredient.objects.create(
            recipe=self.recipe,
            name="salt"
        )
        recipe = Recipe.objects.prefetch_related('ingredients').get(id=self.recipe.id)
        self.assertEqual(recipe.ingredients.count(), 2)

    def test_update_ingredient(self):
        """Test updating an ingredient."""
        ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            quantity=2,
            unit="cups",
            name="flour"
        )
        ingredient.quantity = 3
        ingredient.save()
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.quantity, 3)

    def test_delete_ingredient(self):
        """Test deleting an ingredient."""
        ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            name="flour"
        )
        ingredient_id = ingredient.id
        ingredient.delete()
        self.assertFalse(Ingredient.objects.filter(id=ingredient_id).exists())
        self.assertEqual(self.recipe.ingredients.count(), 0)


class RecipeListViewTest(TestCase):
    """Test cases for RecipeListView."""

    def setUp(self):
        """Set up test data."""
        self.recipe1 = Recipe.objects.create(
            name="Chocolate Chip Cookies",
            description="Delicious homemade cookies",
            instructions="Mix and bake"
        )
        self.recipe2 = Recipe.objects.create(
            name="Chicken Salad",
            description="Quick meal for lunch",
            instructions="Mix ingredients"
        )
        self.recipe3 = Recipe.objects.create(
            name="Flourless Cake",
            description="Gluten-free dessert",
            instructions="Bake cake"
        )
        Ingredient.objects.create(
            recipe=self.recipe1,
            name="chocolate chips"
        )
        Ingredient.objects.create(
            recipe=self.recipe2,
            name="chicken breast"
        )
        Ingredient.objects.create(
            recipe=self.recipe3,
            name="flour"
        )

    def test_list_all_recipes(self):
        """Test that list view displays all recipes when no query is provided."""
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        self.assertEqual(recipes.count(), 3)
        self.assertIn(self.recipe1, recipes)
        self.assertIn(self.recipe2, recipes)
        self.assertIn(self.recipe3, recipes)

    def test_search_by_recipe_name(self):
        """Test searching for recipes by name."""
        response = self.client.get('/recipes/', {'q': 'chocolate'})
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        self.assertIn(self.recipe1, recipes)
        self.assertNotIn(self.recipe2, recipes)
        self.assertNotIn(self.recipe3, recipes)

    def test_search_by_description(self):
        """Test searching for recipes by description."""
        response = self.client.get('/recipes/', {'q': 'quick meal'})
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        self.assertIn(self.recipe2, recipes)
        self.assertNotIn(self.recipe1, recipes)
        self.assertNotIn(self.recipe3, recipes)

    def test_search_by_ingredient_name(self):
        """Test searching for recipes by ingredient name."""
        response = self.client.get('/recipes/', {'q': 'flour'})
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        self.assertIn(self.recipe3, recipes)
        self.assertNotIn(self.recipe1, recipes)
        self.assertNotIn(self.recipe2, recipes)

    def test_search_across_multiple_fields(self):
        """Test searching across name, description, and ingredients."""
        response = self.client.get('/recipes/', {'q': 'chicken'})
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        # Should match recipe2 by name and ingredient
        self.assertIn(self.recipe2, recipes)
        self.assertNotIn(self.recipe1, recipes)
        self.assertNotIn(self.recipe3, recipes)

    def test_case_insensitive_search(self):
        """Test that search is case-insensitive."""
        response = self.client.get('/recipes/', {'q': 'CHOCOLATE'})
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        self.assertIn(self.recipe1, recipes)
        
        response = self.client.get('/recipes/', {'q': 'ChIcKeN'})
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        self.assertIn(self.recipe2, recipes)

    def test_empty_search_query(self):
        """Test handling of empty search query shows all recipes."""
        response = self.client.get('/recipes/', {'q': ''})
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        self.assertEqual(recipes.count(), 3)
        self.assertFalse(response.context['has_query'])

    def test_empty_search_query_with_whitespace(self):
        """Test handling of search query with only whitespace shows all recipes."""
        response = self.client.get('/recipes/', {'q': '   '})
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        self.assertEqual(recipes.count(), 3)
        self.assertFalse(response.context['has_query'])

    def test_no_search_results(self):
        """Test search with no matching results."""
        response = self.client.get('/recipes/', {'q': 'nonexistent'})
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        self.assertEqual(recipes.count(), 0)
        self.assertTrue(response.context['has_query'])

    def test_list_template_rendering(self):
        """Test that list template renders correctly."""
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe Collection')
        self.assertContains(response, self.recipe1.name)

    def test_list_template_with_search(self):
        """Test template rendering with search query."""
        response = self.client.get('/recipes/', {'q': 'chocolate'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'chocolate')
        self.assertContains(response, self.recipe1.name)

    def test_list_template_with_no_results(self):
        """Test template rendering when no results are found."""
        response = self.client.get('/recipes/', {'q': 'nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found')


class RecipeDetailViewTest(TestCase):
    """Test cases for RecipeDetailView."""

    def setUp(self):
        """Set up test data."""
        self.tag1 = Tag.objects.create(name="dessert")
        self.tag2 = Tag.objects.create(name="vegetarian")
        self.recipe = Recipe.objects.create(
            name="Chocolate Chip Cookies",
            description="Delicious homemade cookies",
            servings=24,
            prep_time=15,
            cook_time=12,
            instructions="Mix ingredients and bake at 350F for 12 minutes"
        )
        self.recipe.tags.add(self.tag1, self.tag2)
        Ingredient.objects.create(
            recipe=self.recipe,
            quantity=2.5,
            unit="cups",
            name="flour"
        )
        Ingredient.objects.create(
            recipe=self.recipe,
            quantity=1,
            unit="cup",
            name="sugar"
        )
        Ingredient.objects.create(
            recipe=self.recipe,
            name="chocolate chips"
        )

    def test_detail_view_displays_recipe(self):
        """Test that detail view displays recipe information."""
        response = self.client.get(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recipe'], self.recipe)
        self.assertContains(response, self.recipe.name)
        self.assertContains(response, self.recipe.description)

    def test_detail_view_displays_ingredients(self):
        """Test that detail view displays all ingredients."""
        response = self.client.get(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'flour')
        self.assertContains(response, 'sugar')
        self.assertContains(response, 'chocolate chips')
        self.assertContains(response, '2.5')
        self.assertContains(response, 'cups')

    def test_detail_view_displays_instructions(self):
        """Test that detail view displays instructions."""
        response = self.client.get(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.instructions)

    def test_detail_view_displays_metadata(self):
        """Test that detail view displays recipe metadata."""
        response = self.client.get(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.recipe.servings))
        self.assertContains(response, str(self.recipe.prep_time))
        self.assertContains(response, str(self.recipe.cook_time))

    def test_detail_view_displays_tags(self):
        """Test that detail view displays recipe tags."""
        response = self.client.get(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tag1.name)
        self.assertContains(response, self.tag2.name)

    def test_detail_view_404_for_nonexistent_recipe(self):
        """Test that detail view returns 404 for nonexistent recipe."""
        response = self.client.get('/recipes/99999/')
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template_rendering(self):
        """Test that detail template renders correctly."""
        response = self.client.get(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Back to Recipes')
        self.assertContains(response, self.recipe.name)

    def test_detail_view_with_minimal_recipe(self):
        """Test detail view with recipe that has minimal fields."""
        minimal_recipe = Recipe.objects.create(
            name="Simple Recipe",
            instructions="Just do it"
        )
        response = self.client.get(f'/recipes/{minimal_recipe.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, minimal_recipe.name)
        self.assertContains(response, minimal_recipe.instructions)

