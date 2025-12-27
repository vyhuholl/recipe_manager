# Change: Add recipe list view and recipe detail view

## Why
Users need a way to browse all recipes and view individual recipe details. Currently, the recipe search functionality only shows results when a query is provided, and there's no way to view a complete recipe. This change adds a recipe list view at `/recipes/` that displays all recipes with links to detail pages, integrates search functionality into the list view, and creates a beautiful recipe detail view.

## What Changes
- Add recipe list view at `/recipes/` URL showing all recipes with links to detail pages
- Integrate search functionality into the recipe list view (search filters the list)
- Add recipe detail view for individual recipes showing complete recipe information
- **BREAKING**: Move search from `/recipes/search/` to `/recipes/` (search becomes a filter on the list view)
- Improve template design with modern, beautiful UI

## Impact
- Affected specs: `recipe-search`, `recipe-storage`
- Affected code: 
  - `recipes/views.py` - Add RecipeListView and RecipeDetailView
  - `recipes/urls.py` - Update URL patterns
  - `recipes/templates/recipes/` - Create/update templates for list and detail views

