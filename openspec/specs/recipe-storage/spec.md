# recipe-storage Specification

## Purpose
TBD - created by archiving change add-recipe-storage. Update Purpose after archive.
## Requirements
### Requirement: Recipe Data Model
The system SHALL store recipe data with the following core attributes:
- Recipe name (required, text)
- Description (optional, text)
- Number of servings (optional, integer)
- Preparation time in minutes (optional, integer)
- Cooking time in minutes (optional, integer)
- Instructions (required, text)
- Creation timestamp (automatically set)
- Last modification timestamp (automatically updated)

#### Scenario: Create a new recipe
- **WHEN** a recipe is created with name "Chocolate Chip Cookies" and instructions "Mix ingredients and bake"
- **THEN** the recipe is stored in the database with the provided information
- **AND** creation timestamp is automatically set
- **AND** the recipe can be retrieved by its unique identifier

#### Scenario: Recipe requires name and instructions
- **WHEN** attempting to create a recipe without a name
- **THEN** the operation fails with a validation error
- **WHEN** attempting to create a recipe without instructions
- **THEN** the operation fails with a validation error

### Requirement: Ingredient Storage
The system SHALL store ingredients associated with recipes, where each ingredient has:
- Quantity (optional, decimal number)
- Unit of measurement (optional, text, e.g., "cups", "tablespoons", "grams")
- Ingredient name (required, text)
- Association with a recipe (required)

#### Scenario: Add ingredients to a recipe
- **WHEN** creating a recipe with ingredients "2 cups flour", "1 cup sugar", "3 eggs"
- **THEN** each ingredient is stored with its quantity, unit, and name
- **AND** all ingredients are associated with the recipe
- **AND** ingredients can be retrieved as part of the recipe

#### Scenario: Ingredient requires name
- **WHEN** attempting to create an ingredient without a name
- **THEN** the operation fails with a validation error

### Requirement: Recipe Tagging
The system SHALL support tagging recipes with categories or labels for organization. Each tag has:
- Tag name (required, text, unique)
- Association with one or more recipes (many-to-many relationship)

#### Scenario: Tag a recipe
- **WHEN** a recipe is tagged with "dessert" and "vegetarian"
- **THEN** the tags are stored and associated with the recipe
- **AND** the recipe can be filtered or searched by these tags

#### Scenario: Tag names are unique
- **WHEN** attempting to create a tag with a name that already exists
- **THEN** the existing tag is reused
- **AND** the recipe is associated with the existing tag

### Requirement: Recipe Retrieval
The system SHALL support retrieving recipes by:
- Unique identifier
- All recipes (list view)
- Filtering by tags

#### Scenario: Retrieve recipe by ID
- **WHEN** requesting a recipe by its unique identifier
- **THEN** the complete recipe data is returned including name, description, ingredients, instructions, and tags

#### Scenario: List all recipes
- **WHEN** requesting all recipes
- **THEN** a list of all stored recipes is returned with their basic information

#### Scenario: Filter recipes by tag
- **WHEN** requesting recipes filtered by tag "dessert"
- **THEN** only recipes tagged with "dessert" are returned

### Requirement: Recipe Updates
The system SHALL support updating existing recipes, including:
- Modifying recipe fields (name, description, instructions, etc.)
- Adding or removing ingredients
- Adding or removing tags
- Automatically updating the modification timestamp

#### Scenario: Update recipe information
- **WHEN** updating a recipe's name from "Cookies" to "Chocolate Chip Cookies"
- **THEN** the recipe is updated with the new name
- **AND** the modification timestamp is updated
- **AND** other recipe data remains unchanged

#### Scenario: Add ingredient to existing recipe
- **WHEN** adding a new ingredient "1 tsp vanilla" to an existing recipe
- **THEN** the ingredient is added to the recipe's ingredient list
- **AND** existing ingredients remain unchanged

### Requirement: Recipe Deletion
The system SHALL support deleting recipes from storage.

#### Scenario: Delete a recipe
- **WHEN** a recipe is deleted
- **THEN** the recipe is removed from the database
- **AND** associated ingredients are removed (cascade delete)
- **AND** tag associations are removed (but tags themselves remain for reuse)

