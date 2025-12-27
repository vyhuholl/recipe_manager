## ADDED Requirements
### Requirement: Recipe List View
The system SHALL provide a list view at `/recipes/` that displays all recipes with links to their detail pages. The list view SHALL support search filtering to narrow down displayed recipes.

#### Scenario: View all recipes
- **WHEN** a user navigates to `/recipes/`
- **THEN** all recipes are displayed in a list
- **AND** each recipe in the list shows its name and description (if available)
- **AND** each recipe has a link to its detail page

#### Scenario: List view with search
- **WHEN** a user navigates to `/recipes/` with a search query parameter
- **THEN** the list is filtered to show only matching recipes
- **AND** the search form displays the current query
- **AND** users can clear the search to see all recipes again

### Requirement: Recipe Detail View
The system SHALL provide a detail view for individual recipes that displays complete recipe information including name, description, ingredients, instructions, tags, and metadata (servings, prep time, cook time).

#### Scenario: View recipe details
- **WHEN** a user navigates to a recipe detail page (e.g., `/recipes/1/`)
- **THEN** the complete recipe information is displayed including:
  - Recipe name
  - Description (if available)
  - All ingredients with quantities, units, and names
  - Complete instructions
  - Tags (if any)
  - Servings, prep time, and cook time (if available)
  - Creation and modification timestamps

#### Scenario: Navigate to detail from list
- **WHEN** a user clicks a recipe link in the list view
- **THEN** they are navigated to that recipe's detail page
- **AND** the detail page displays the complete recipe information

