import streamlit as st
import json
import os
from PIL import Image

# Ensure folders exist
os.makedirs("images", exist_ok=True)

# Load recipes from file
def load_recipes():
    if os.path.exists("recipes.json"):
        with open("recipes.json", "r") as f:
            return json.load(f)
    return []

# Save new recipe
def save_recipe(data):
    recipes = load_recipes()
    recipes.append(data)
    with open("recipes.json", "w") as f:
        json.dump(recipes, f, indent=4)

# Delete recipe
def delete_recipe(index):
    recipes = load_recipes()
    recipes.pop(index)
    with open("recipes.json", "w") as f:
        json.dump(recipes, f, indent=4)

# Categories
categories = [
    "FastFood", "Dasi", "SeaFood", "Desserts", "Beverages", "Vegetarian", "Healthy",
    "Vegan", "Grilled", "Salads", "Soups", "Breakfast", "Pasta", "Snacks", "Rice", "Baked"
]

# App title
st.set_page_config(page_title="🍽️ Recipe Generator", layout="wide")
st.title("👨‍🍳 Public Recipe Library")

# Sidebar navigation with increased heading font size
# Sidebar navigation with even larger heading font size
with st.sidebar:
    st.markdown("<h1 style='font-size: 36px; font-weight: bold;'>Navigation</h1>", unsafe_allow_html=True)
    menu = st.radio(
        label="Select a page:",
        options=["➕ Add Recipe", "📚 View Recipes", "🔍 Search Recipes"],
        index=0,
        help="Choose the section to navigate to",
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size: 28px; font-weight: bold;'>Categories</h2>", unsafe_allow_html=True)
    st.write("Browse recipes by category")

# --- Add Recipe ---
if menu == "➕ Add Recipe":
    st.subheader("➕ Add a New Recipe")

    with st.form("add_form"):
        title = st.text_input("Recipe Title")
        category = st.selectbox("Category", categories)
        ingredients = st.text_area("Ingredients (comma separated)")
        steps = st.text_area("Preparation Steps")
        image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

        submit = st.form_submit_button("Save Recipe")

        if submit and title and image:
            image_path = f"images/{image.name}"
            with open(image_path, "wb") as f:
                f.write(image.read())

            new = {
                "title": title,
                "category": category,
                "ingredients": [i.strip() for i in ingredients.split(",")],
                "steps": steps,
                "image": image_path
            }
            save_recipe(new)
            st.success("✅ Recipe saved successfully!")

# --- View Recipes ---
elif menu == "📚 View Recipes":
    st.subheader("📖 All Recipes")
    recipes = load_recipes()

    page_size = st.slider("Select number of recipes per page", 5, 50, 10)
    total_pages = max(1, (len(recipes) + page_size - 1) // page_size)
    page_num = st.number_input("Select Page", 1, total_pages, 1)

    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    paged_recipes = recipes[start_index:end_index]

    for index, r in enumerate(paged_recipes, start=start_index):
        with st.container():
            cols = st.columns([1, 2])
            if "image" in r and os.path.exists(r["image"]):
                try:
                    img = Image.open(r["image"])
                    cols[0].image(img, use_container_width=True)
                except Exception as e:
                    cols[0].warning(f"Error loading image: {e}")
            else:
                cols[0].warning("No Image")

            with cols[1]:
                st.markdown(f"### 🍲 {r['title']}")
                st.write(f"**📁 Category:** {r['category']}")
                st.write("**🧂 Ingredients:**", ", ".join(r["ingredients"]))
                st.write("**📋 Steps:**", r["steps"])
                delete_button = st.button("❌ Delete", key=f"delete_{index}")
                if delete_button:
                    delete_recipe(index)
                    st.warning("❌ Recipe deleted successfully!")
                    st.rerun()
                st.markdown("---")

# --- Search Recipes ---
elif menu == "🔍 Search Recipes":
    st.subheader("🔎 Search Recipes")
    category_filter = st.selectbox("Select Category", ["All"] + categories)
    search_query = st.text_input("Search by Recipe Title or Ingredient")

    if search_query or category_filter != "All":
        recipes = load_recipes()

        if category_filter != "All":
            recipes = [r for r in recipes if r["category"] == category_filter]

        search_results = [
            r for r in recipes if search_query.lower() in r['title'].lower() or any(search_query.lower() in ingredient.lower() for ingredient in r['ingredients'])
        ]

        page_size = st.slider("Select number of recipes per page", 5, 50, 10)
        total_pages = max(1, (len(search_results) + page_size - 1) // page_size)
        page_num = st.number_input("Select Page", 1, total_pages, 1)

        start_index = (page_num - 1) * page_size
        end_index = start_index + page_size
        paged_search_results = search_results[start_index:end_index]

        if paged_search_results:
            for r in paged_search_results:
                with st.container():
                    cols = st.columns([1, 2])
                    if "image" in r and os.path.exists(r["image"]):
                        try:
                            img = Image.open(r["image"])
                            cols[0].image(img, use_container_width=True)
                        except Exception as e:
                            cols[0].warning(f"Error loading image: {e}")
                    else:
                        cols[0].warning("No Image")

                    with cols[1]:
                        st.markdown(f"### 🍲 {r['title']}")
                        st.write(f"**📁 Category:** {r['category']}")
                        st.write("**🧂 Ingredients:**", ", ".join(r["ingredients"]))
                        st.write("**📋 Steps:**", r["steps"])
                    st.markdown("---")
        else:
            st.warning("No recipes found for your search query.")

# Footer
st.markdown("""
    <hr>
    <footer style='text-align: center; font-size: 14px; color: gray;'>
        <p>&copy; 2025 All rights reserved | Ubaid-ur-Rehman</p>
    </footer>
""", unsafe_allow_html=True)
