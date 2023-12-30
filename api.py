import pandas as pd
import pathway as pw
import os
from dotenv import load_dotenv
from common.prompt import prompt

# Load environment variables from .env file
load_dotenv()

# Path to your dataset
dataset_path = os.environ.get("RECIPE_DATASET_LOCAL_PATH", "/usr/local/documents")

def run(host, port):
    user_input, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=UserInputSchema,
        autocommit_duration_ms=50,
    )

    recipes = get_recipe_suggestions(user_input)  # Fetch recipes based on user input

    formatted_response = format_recipes(recipes)  # Format recipes for display

    response_writer(formatted_response)  # Provide the formatted response to the user

    pw.run()

class UserInputSchema(pw.Schema):
    # Define the expected user input schema, e.g., user query, dietary preferences, ingredients
    query: str
    # Add other user input fields as needed, such as dietary preferences, ingredients, etc.

def get_recipe_suggestions(user_input):
    # Load the dataset containing recipe information
    recipes_df = pd.read_csv(dataset_path)

    # Filter recipes based on the user's query matching relevant columns (e.g., name, tags, description, ingredients)
    filtered_recipes = recipes_df[
        (recipes_df['name'].str.contains(user_input['query'], case=False)) |
        (recipes_df['tags'].str.contains(user_input['query'], case=False)) |
        (recipes_df['description'].str.contains(user_input['query'], case=False)) |
        (recipes_df['ingredients'].str.contains(user_input['query'], case=False))
    ]

    # Convert the filtered recipes to a list of dictionaries for easier handling
    suggested_recipes = filtered_recipes.to_dict(orient='records')

    return suggested_recipes


def format_recipes(recipes):
    formatted_response = ""

    # Iterate through the retrieved recipes and format them for display
    for index, recipe in enumerate(recipes, start=1):
        formatted_response += f"Recipe {index}:\n"
        formatted_response += f"Name: {recipe['name']}\n"
        formatted_response += f"Minutes: {recipe['minutes']}\n"
        formatted_response += f"Tags: {recipe['tags']}\n"
        formatted_response += f"Description: {recipe['description']}\n"
        formatted_response += f"Ingredients: {recipe['ingredients']}\n\n"

    return formatted_response

# Entry point to run the LLM App
if __name__ == "__main__":
    run("localhost", 8080)  # Replace host and port with your desired values
