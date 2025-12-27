from django.db import models
from django.core.validators import MinValueValidator


class Tag(models.Model):
    """Tag model for categorizing recipes."""
    name = models.CharField(max_length=50, unique=True, help_text="Tag name")

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Recipe model storing core recipe information."""
    name = models.CharField(max_length=200, help_text="Recipe name")
    description = models.TextField(blank=True, help_text="Optional recipe description")
    servings = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Number of servings"
    )
    prep_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Preparation time in minutes"
    )
    cook_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Cooking time in minutes"
    )
    instructions = models.TextField(help_text="Recipe instructions")
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
        help_text="Tags for categorizing this recipe"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Ingredient model for recipe ingredients."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        help_text="Recipe this ingredient belongs to"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Ingredient quantity"
    )
    unit = models.CharField(
        max_length=50,
        blank=True,
        help_text="Unit of measurement (e.g., cups, tablespoons, grams)"
    )
    name = models.CharField(max_length=200, help_text="Ingredient name")

    class Meta:
        ordering = ['recipe', 'name']
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self) -> str:
        if self.quantity and self.unit:
            return f"{self.quantity} {self.unit} {self.name}"
        elif self.quantity:
            return f"{self.quantity} {self.name}"
        else:
            return self.name

