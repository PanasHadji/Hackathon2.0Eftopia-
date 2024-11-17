from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
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
    similarity: int
    trust: int
    summary: str
    verdict: str
    date: str
    categories: List[Category]
    categoryPercentages: List[CategoryPercentage]
    radarData: List[RadarData]

# Define the SearchRequest model
class SearchRequest(BaseModel):
    query: str

# Dummy or Template Data for Court Cases
def generate_court_cases(query: str) -> List[CourtCase]:
    # Here, we return some static or generated data for now
    from typing import List
    
    class ChildCategory:
        def __init__(self, name: str, value: int, children: List = None):
            self.name = name
            self.value = value
            self.children = children if children is not None else []
    
    class Category:
        def __init__(self, name: str, value: int, children: List[ChildCategory]):
            self.name = name
            self.value = value
            self.children = children
    
    class CategoryPercentage:
        def __init__(self, category: str, value: int):
            self.category = category
            self.value = value
    
    class RadarData:
        def __init__(self, category: str, value: int):
            self.category = category
            self.value = value
    
    class CourtCase:
        def __init__(self, id: int, caseName: str, caseNumber: str, summary: str, verdict: str, date: str, categories: List[Category], categoryPercentages: List[CategoryPercentage], radarData: List[RadarData]):
            self.id = id
            self.caseName = caseName
            self.caseNumber = caseNumber
            self.summary = summary
            self.verdict = verdict
            self.date = date
            self.categories = categories
            self.categoryPercentages = categoryPercentages
            self.radarData = radarData
   
   
def generate_court_cases() -> List[CourtCase]:
    return [
          CourtCase(
              id=1,
              caseName="Case of Immigration Policy",
              caseNumber="2023-IM-001",
              similarity=87,
              trust=93,
              summary="A case regarding the recent changes in immigration policies and their legal implications. The case challenges the constitutional validity of new immigration laws that may affect the rights of refugees and asylum seekers. The legal dispute centers around whether the new policies are in line with international human rights obligations and the provisions for asylum as set forth by the United Nations.",
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
              caseName="Case of Environmental Protection",
              caseNumber="2023-EN-002",
              similarity=75,
              trust=79,
              summary="This case involves the legal challenges brought against a corporation for alleged environmental violations. The company is accused of causing widespread pollution through its manufacturing processes, leading to significant environmental damage. The case explores environmental law in the context of corporate responsibility, as well as the legal obligations of companies under national and international environmental standards. The ruling will have far-reaching implications for environmental policy and corporate accountability.",
              verdict="Pending decision.",
              date="2023-07-19",
              categories=[ 
                  Category(
                      name="Environmental Law",
                      value=60,
                      children=[
                          ChildCategory(name="Pollution Control", value=30),
                          ChildCategory(name="Wildlife Protection", value=30)
                      ]
                  ),
                  Category(
                      name="Corporate Law",
                      value=40,
                      children=[
                          ChildCategory(name="Business Ethics", value=20),
                          ChildCategory(name="Corporate Governance", value=20)
                      ]
                  )
              ],
              categoryPercentages=[ 
                  CategoryPercentage(category="Environmental Protection", value=70),
                  CategoryPercentage(category="Corporate Responsibility", value=20),
                  CategoryPercentage(category="Public Health Law", value=10)
              ],
              radarData=[ 
                  RadarData(category="Environmental Protection", value=90),
                  RadarData(category="Corporate Responsibility", value=50),
                  RadarData(category="Public Health Law", value=60)
              ]
          ),
          CourtCase(
              id=3,
              caseName="Case of Financial Mismanagement",
              caseNumber="2023-FM-003",
              similarity=79,
              trust=89,
              summary="This case involves a major financial institution accused of mismanaging funds, leading to severe losses for its investors. The institution allegedly failed to comply with financial regulations regarding transparency and reporting, resulting in a breach of fiduciary duties. The case examines the intersection of financial law, corporate accountability, and investor protection. Legal experts anticipate that the outcome will establish new precedents for financial regulation and the responsibilities of corporate executives.",
              verdict="Pending ruling.",
              date="2023-08-25",
              categories=[ 
                  Category(
                      name="Financial Law",
                      value=70,
                      children=[
                          ChildCategory(name="Fraudulent Activities", value=35),
                          ChildCategory(name="Investment Regulation", value=35)
                      ]
                  ),
                  Category(
                      name="Corporate Law",
                      value=30,
                      children=[
                          ChildCategory(name="Corporate Governance", value=15),
                          ChildCategory(name="Executive Accountability", value=15)
                      ]
                  )
              ],
              categoryPercentages=[ 
                  CategoryPercentage(category="Financial Mismanagement", value=85),
                  CategoryPercentage(category="Investor Protection", value=10),
                  CategoryPercentage(category="Corporate Governance", value=5)
              ],
              radarData=[ 
                  RadarData(category="Financial Mismanagement", value=95),
                  RadarData(category="Investor Protection", value=60),
                  RadarData(category="Corporate Governance", value=50)
              ]
          )
      ]


# POST endpoint for search and classification
@app.post("/search")
async def search(request: SearchRequest):

    text = request.query
    result = nlp_pipeline(text, law_categories)
    predicted_label = result["labels"][0]
    probabilities = dict(zip(result["labels"], result["scores"]))
    
    # Generate dummy court case data for now (this can be made dynamic based on the classification)
    return generate_court_cases()

# Root endpoint for health check
@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Case Classifier API!"}
