from fastapi import FastAPI, Request
from transformers import pipeline
from pydantic import BaseModel
import torch

# Initialize the FastAPI app
app = FastAPI()

# Load the Bert Model and Pipeline
model_name = "nlpaueb/legal-bert-base-uncased"
nlp_pipeline = pipeline("zero-shot-classification", model=model_name)

# The labels for the crime committed
law_categories = [
    "Civil and Political Rights", "Environmental Law",
    "Immigration Law", "Financial Law", "Family Law",
    "IP Law", "Commercial Law", "International Law"
]

# Define request model for input data
class SearchRequest(BaseModel):
    query: str
    # You can add additional filters or parameters here if needed
    # e.g., filters: Optional[List[str]]

# Define response model for the /search endpoint
@app.post("/search")
async def search(request: SearchRequest):
    text = request.query

    # Perform zero-shot classification using the pipeline
    result = nlp_pipeline(text, law_categories)

    # Get the most likely label and associated probabilities
    predicted_label = result["labels"][0]
    probabilities = dict(zip(result["labels"], result["scores"]))

    return {
        "query": text,
        "predicted_label": predicted_label,
        "probabilities": probabilities,
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Case Classifier API!"}
