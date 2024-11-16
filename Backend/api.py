from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

# Initialize the FastAPI app
app = FastAPI()

# Load the model and pipeline
model_name = "nlpaueb/legal-bert-base-uncased"
nlp_pipeline = pipeline("zero-shot-classification", model=model_name)

# Your classification categories
law_categories = [
    "Civil and Political Rights", "Environmental Law", "Immigration Law",
    "Financial Law", "Family Law", "IP Law", "Commercial Law", "International Law"
]

# Define the SearchRequest model
class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search(request: SearchRequest):
    text = request.query
    result = nlp_pipeline(text, law_categories)
    predicted_label = result["labels"][0]
    probabilities = dict(zip(result["labels"], result["scores"]))
    return {"query": text, "predicted_label": predicted_label, "probabilities": probabilities}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Case Classifier API!"}
