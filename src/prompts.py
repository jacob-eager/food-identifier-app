def generate_prompt(food_name):
    prompt = f"""
You are tasked with generating a recipe for the given food name.

**Requirements:**
- Include a complete list of ingredients with quantities.
- Include clear, numbered preparation steps.
- Use common household measurements when possible.
- The recipe must be self-contained and ready to cook from.
- Do NOT include any text outside the specified delimiters.
- Do NOT add explanations, commentary, or extra markdown.

### Output Format (use these delimiters exactly):

RECIPE_START
<Recipe>
RECIPE_END

---
