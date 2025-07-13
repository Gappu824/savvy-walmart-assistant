from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import json
import re
import os

# --- Configuration ---
# In a real app, use environment variables for keys
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY", "d6e16aadf7ea4e0c81987b07c22fcf04")
BASE_MODEL_ID = "/model"
ADAPTER_PATH = "./walmart-savvy-finetuned"

# --- Load the Fine-Tuned Model ---
# This happens once when the service starts up
print("Loading fine-tuned model...")
base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_ID, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
print("Model loaded successfully.")

app = FastAPI(title="Recommendation Service")

class RecommendRequest(BaseModel):
    user_id: int
    query_text: str

@app.post("/recommend")
async def get_recommendations(request: RecommendRequest):
    # Step 1: Use your fine-tuned model to parse the user's query
    prompt = f"<|user|>\nParse the query: '{request.query_text}'<|end|>\n<|assistant|>\n" + "{"
    inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False)
    outputs = model.generate(**inputs, max_new_tokens=200, eos_token_id=tokenizer.eos_token_id)
    raw_output = tokenizer.batch_decode(outputs)[0]

    try:
        json_part = "{" + raw_output.split("<|assistant|>")[1].replace("{", "", 1).replace("<|end|>", "").strip()
        structured_query = json.loads(json_part)
    except Exception:
        # If the model fails, use the query text as a fallback keyword
        structured_query = {"keywords": [request.query_text]}

    # In a full implementation, you would also call the user_service and community_service here
    # to get pantry items, user preferences, and trending data. We will omit this for simplicity now.

    # Step 2: Call the external Spoonacular API with the parsed keywords
    async with httpx.AsyncClient() as client:
        params = {
            "apiKey": SPOONACULAR_API_KEY,
            "query": ", ".join(structured_query.get("keywords", [])),
            "number": 10, # Get 10 recipes
        }
        # Add diet from AI parsing if available
        if structured_query.get("diet"):
            params["diet"] = structured_query["diet"]

        try:
            print(f"Querying Spoonacular with params: {params}")
            response = await client.get("https://api.spoonacular.com/recipes/complexSearch", params=params)
            response.raise_for_status() # Raise an exception for bad status codes
            recipes = response.json().get("results", [])
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Error contacting Spoonacular API: {exc}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process recipes: {e}")

    return {"recipes": recipes}