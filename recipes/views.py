from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Recipe


class RecipeListView(ListView):
    """View for listing all recipes with optional search filtering."""
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'
    paginate_by = None

    def get_queryset(self):
        """Filter recipes based on search query, or return all if no query."""
        query = self.request.GET.get('q', '').strip()
        
        queryset = Recipe.objects.all()
        
        if query:
            # Search across recipe name, description, and ingredient names
            # Case-insensitive search using icontains
            queryset = queryset.filter(
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


class RecipeDetailView(DetailView):
    """View for displaying individual recipe details."""
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'
    pk_url_kwarg = 'id'

