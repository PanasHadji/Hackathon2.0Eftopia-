from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from pydantic import BaseModel
from docx import Document
import PyPDF2
from bs4 import BeautifulSoup

# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Load the model and pipeline
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



#parse dawgx
def parse_docx(file_path):
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

#parse pdf
def parse_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
        return '\n'.join(text)

#parse html
def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        text = soup.get_text()
    return text





@app.post("/search")
async def search(request: SearchRequest):

    text = request.query

    #fetched_cases = ??

    result = nlp_pipeline(text, law_categories)
    predicted_label = result["labels"][0]
    probabilities = dict(zip(result["labels"], result["scores"]))
    return {"query": text, "predicted_label": predicted_label, "probabilities": probabilities} #TODO "cases": fetched_cases

@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Case Classifier API!"}
