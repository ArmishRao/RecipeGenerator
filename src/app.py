from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, FlaxT5ForConditionalGeneration
import jax.numpy as jnp

app = Flask(__name__)

# Load model + tokenizer
model_name = "flax-community/t5-recipe-generation"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = FlaxT5ForConditionalGeneration.from_pretrained(model_name, force_download=True)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_recipe():
    ingredients = request.form["ingredients"]

    prompt = f"ingredients: {ingredients} recipe:"

    inputs = tokenizer(prompt, return_tensors="jax")
    output_ids = model.generate(
        input_ids=inputs["input_ids"],
        max_length=200
    ).sequences

    recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return jsonify({"recipe": recipe})

if __name__ == "__main__":
    app.run(debug=True)
