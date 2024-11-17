from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from docx import Document
import PyPDF2
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# Initialize the FastAPI app
app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model and zero-shot classification pipeline
model_name = "nlpaueb/legal-bert-base-uncased"
nlp_pipeline = pipeline("zero-shot-classification", model=model_name)

# Define classification categories for legal cases
law_categories = [
    "Civil and Political Rights", "Environmental Law", "Immigration Law",
    "Financial Law", "Family Law", "IP Law", "Commercial Law", "International Law"
]

# Define Pydantic models for the data structure
class ChildCategory(BaseModel):
    name: str
    value: int

class Category(BaseModel):
    name: str
    value: int
    children: List[ChildCategory]

class CategoryPercentage(BaseModel):
    category: str
    value: int

class RadarData(BaseModel):
    category: str
    value: int

class CourtCase(BaseModel):
    id: int
    caseName: str
    caseNumber: str
    summary: str
    verdict: str
    date: str
    categories: List[Category]
    categoryPercentages: List[CategoryPercentage]
    radarData: List[RadarData]

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





# Dummy or Template Data for Court Cases
def generate_court_cases(query: str) -> List[CourtCase]:
    # Here, we return some static or generated data for now
    return [
        CourtCase(
            id=1,
            caseName="Case of Immigration Policy",
            caseNumber="2023-IM-001",
            summary="A case regarding the recent changes in immigration policies and their legal implications.",
            verdict="In favor of the plaintiff.",
            date="2023-05-12",
            categories=[ 
                Category(
                    name="Immigration Law",
                    value=35,
                    children=[
                        ChildCategory(name="Visa Policy", value=20),
                        ChildCategory(name="Refugee Law", value=15)
                    ]
                ),
                Category(
                    name="Financial Law",
                    value=45,
                    children=[
                        ChildCategory(name="Taxation", value=25),
                        ChildCategory(name="Investment Law", value=20)
                    ]
                ),
                Category(
                    name="Criminal Law",
                    value=20,
                    children=[
                        ChildCategory(name="White-collar Crimes", value=10),
                        ChildCategory(name="Violent Crimes", value=10)
                    ]
                )
            ],
            categoryPercentages=[ 
                CategoryPercentage(category="Antitrust Law", value=55),
                CategoryPercentage(category="Corporate Law", value=30),
                CategoryPercentage(category="Technology Law", value=15)
            ],
            radarData=[ 
                RadarData(category="Antitrust Law", value=80),
                RadarData(category="Corporate Law", value=60),
                RadarData(category="Technology Law", value=50)
            ]
        ),
         CourtCase(
                    id=2,
                    caseName="Case",
                    caseNumber="2023-IM-001",
                    summary="A case regarding the recent changes in immigration policies and their legal implications.",
                    verdict="In favor of the plaintiff.",
                    date="2023-05-12",
                    categories=[ 
                        Category(
                            name="Immigration Law",
                            value=35,
                            children=[
                                ChildCategory(name="Visa Policy", value=20, children=[]),
                                ChildCategory(name="Refugee Law", value=15, children=[])
                            ]
                        ),
                        Category(
                            name="Financial Law",
                            value=45,
                            children=[
                                ChildCategory(name="Taxation", value=25, children=[]),
                                ChildCategory(name="Investment Law", value=20, children=[])
                            ]
                        ),
                        Category(
                            name="Criminal Law",
                            value=20,
                            children=[
                                ChildCategory(name="White-collar Crimes", value=10, children=[]),
                                ChildCategory(name="Violent Crimes", value=10, children=[])
                            ]
                        )
                    ],
                    categoryPercentages=[ 
                        CategoryPercentage(category="Antitrust Law", value=55),
                        CategoryPercentage(category="Corporate Law", value=30),
                        CategoryPercentage(category="Technology Law", value=15)
                    ],
                    radarData=[ 
                        RadarData(category="Antitrust Law", value=80),
                        RadarData(category="Corporate Law", value=60),
                        RadarData(category="Technology Law", value=50)
                    ]
                ),
    ]

# POST endpoint for search and classification
@app.post("/search")
async def search(request: SearchRequest):

    text = request.query
    result = nlp_pipeline(text, law_categories)
    predicted_label = result["labels"][0]
    probabilities = dict(zip(result["labels"], result["scores"]))
    
    # Generate dummy court case data for now (this can be made dynamic based on the classification)
    return generate_court_cases(text)

# Root endpoint for health check
@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Case Classifier API!"}
