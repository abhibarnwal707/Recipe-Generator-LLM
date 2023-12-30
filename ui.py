import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "api")
api_port = int(os.environ.get("PORT", 8080))


# Streamlit UI elements
st.title("Recipe Suggestion LLM App")

dietary_preferences = st.text_input(
    "Enter your dietary preferences",
    placeholder="e.g., vegetarian, gluten-free, keto-friendly"
)

ingredients = st.text_input(
    "Enter ingredients you have",
    placeholder="e.g., chicken, tomatoes, onions"
)

cooking_instructions = st.text_input(
    "Any specific cooking instructions?",
    placeholder="e.g., bake, grill, sauté"
)

if st.button("Get Recipe Suggestions"):
    # Construct user query
    query = {
        "dietary_preferences": dietary_preferences,
        "ingredients": ingredients,
        "cooking_instructions": cooking_instructions
    }

    # Send query to LLM App
    url = f'http://{api_host}:{api_port}/'
    response = requests.post(url, json=query)

    if response.status_code == 200:
        st.write("### Recipe Suggestions")
        suggested_recipes = response.json()
        for recipe in suggested_recipes:
            st.write(f"- {recipe['name']}: {recipe['description']}")
            st.write(f"  Ingredients: {recipe['ingredients']}")
            st.write(f"  Cooking Instructions: {recipe['steps']}")
    else:
        st.error(f"Failed to fetch recipe suggestions. Status code: {response.status_code}")
