from django.views.generic import ListView
from django.db.models import Q
from .models import Recipe


class RecipeSearchView(ListView):
    """View for searching recipes by name, description, or ingredient names."""
    model = Recipe
    template_name = 'recipes/search.html'
    context_object_name = 'recipes'
    paginate_by = None

    def get_queryset(self):
        """Filter recipes based on search query."""
        query = self.request.GET.get('q', '').strip()
        
        if not query:
            return Recipe.objects.none()
        
        # Search across recipe name, description, and ingredient names
        # Case-insensitive search using icontains
        queryset = Recipe.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__name__icontains=query)
        ).distinct()
        
        return queryset

    def get_context_data(self, **kwargs):
        """Add search query to context."""
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        context['has_query'] = bool(context['query'])
        return context

