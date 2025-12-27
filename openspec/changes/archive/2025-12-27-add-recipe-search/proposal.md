# Change: Add Recipe Search

## Why
Users need to find recipes quickly by searching across recipe names, descriptions, ingredients, and other attributes. Currently, recipes can only be filtered by tags, which limits discoverability. A search interface will improve user experience by enabling flexible text-based recipe discovery.

## What Changes
- Add a search view that accepts query parameters and returns matching recipes
- Create a search template with a search form and results display
- Support searching across recipe names, descriptions, and ingredient names
- Display search results with basic recipe information
- Handle empty search queries gracefully

## Impact
- Affected specs: `recipe-search` (new capability)
- Affected code:
  - New: `recipes/views.py` (search view)
  - New: `recipes/urls.py` (URL routing)
  - New: `recipes/templates/recipes/search.html` (search template)
  - Modified: `recipe_manager/urls.py` (include recipes URLs)

