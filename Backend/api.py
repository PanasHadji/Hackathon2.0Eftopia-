from fastapi import FastAPI, Request
from transformers import pipeline
from pydantic import BaseModel
import torch

# Initialize the FastAPI app
app = FastAPI()

# Load the Bert Model and PipeLine
model_name = "nlpaueb/legal-bert-base-uncased"
nlp_pipeline = pipeline("zero-shot-classification", model=model_name)

#the labels for the crime commited
law_categories = ["Civil and Political Rights", "Enviromental Law",
                  "Immigration Law", "Financial Law", "Family Law",
                  "IP Law", "Commercial Law", "International Law"]

#dummy test
text = "The defendant shot his wife 8 times in the face."

# Define request model for input data
class SearchRequest(BaseModel):
    query: str
    #TODO add filters

# Endpoint for zero-shot classification
@app.post("/predict")
async def predict(request: SearchRequest):
    text = request.query
    law_categories = request.law_categories

    # Perform zero-shot classification
    result = nlp_pipeline(text, law_categories)

    # Get the most likely label
    predicted_label = result["labels"][0]
    probabilities = result["scores"]

    return {
        "predicted_label": predicted_label,
        "probabilities": dict(zip(result["labels"], probabilities)),
    }
@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Case Classifier API!"}