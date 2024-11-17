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
    language: str

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
   
   
from typing import List

# Define the necessary classes for CourtCase, Category, ChildCategory, etc.

class ChildCategory:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

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
    def __init__(self, id: int, caseName: str, caseNumber: str, similarity: int, trust: int,
                 summary: str, verdict: str, date: str, categories: List[Category],
                 categoryPercentages: List[CategoryPercentage], radarData: List[RadarData]):
        self.id = id
        self.caseName = caseName
        self.caseNumber = caseNumber
        self.similarity = similarity
        self.trust = trust
        self.summary = summary
        self.verdict = verdict
        self.date = date
        self.categories = categories
        self.categoryPercentages = categoryPercentages
        self.radarData = radarData

def generate_court_cases(language: str) -> List[CourtCase]:
    if language == "English":
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
    
    elif language == "Greek":  # Greek
        return [
            CourtCase(
                id=1,
                caseName="Υπόθεση Πολιτικής Μετανάστευσης",
                caseNumber="2023-IM-001",
                similarity=87,
                trust=93,
                summary="Μια υπόθεση που αφορά τις πρόσφατες αλλαγές στις πολιτικές μετανάστευσης και τις νομικές τους συνέπειες. Η υπόθεση αμφισβητεί τη συνταγματική εγκυρότητα των νέων νόμων για τη μετανάστευση που ενδέχεται να επηρεάσουν τα δικαιώματα των προσφύγων και των αιτούντων άσυλο. Η νομική διαμάχη αφορά το αν οι νέες πολιτικές είναι σύμφωνες με τις διεθνείς υποχρεώσεις για τα ανθρώπινα δικαιώματα και τις διατάξεις για το άσυλο που προβλέπονται από τον ΟΗΕ.",
                verdict="Υπέρ του ενάγοντος.",
                date="2023-05-12",
                categories=[
                    Category(
                        name="Νόμος Μετανάστευσης",
                        value=35,
                        children=[
                            ChildCategory(name="Πολιτική Θεώρησης", value=20),
                            ChildCategory(name="Νόμος για τους Πρόσφυγες", value=15)
                        ]
                    ),
                    Category(
                        name="Χρηματοοικονομικός Νόμος",
                        value=45,
                        children=[
                            ChildCategory(name="Φορολογία", value=25),
                            ChildCategory(name="Νόμος για τις Επενδύσεις", value=20)
                        ]
                    ),
                    Category(
                        name="Ποινικός Νόμος",
                        value=20,
                        children=[
                            ChildCategory(name="Εγκλήματα Λευκού Κολάρου", value=10),
                            ChildCategory(name="Βίαια Εγκλήματα", value=10)
                        ]
                    )
                ],
                categoryPercentages=[
                    CategoryPercentage(category="Αντικανονικός Νόμος", value=55),
                    CategoryPercentage(category="Εταιρικός Νόμος", value=30),
                    CategoryPercentage(category="Νόμος για την Τεχνολογία", value=15)
                ],
                radarData=[
                    RadarData(category="Αντικανονικός Νόμος", value=80),
                    RadarData(category="Εταιρικός Νόμος", value=60),
                    RadarData(category="Νόμος για την Τεχνολογία", value=50)
                ]
            ),
        ]

    elif language == "French":  # French
        return [
            CourtCase(
                id=1,
                caseName="Affaire de Politique Migratoire",
                caseNumber="2023-IM-001",
                similarity=87,
                trust=93,
                summary="Une affaire concernant les récentes modifications des politiques migratoires et leurs implications juridiques. L'affaire remet en question la validité constitutionnelle des nouvelles lois sur l'immigration qui peuvent affecter les droits des réfugiés et des demandeurs d'asile. Le litige juridique porte sur la question de savoir si les nouvelles politiques sont conformes aux obligations internationales en matière de droits humains et aux dispositions relatives à l'asile énoncées par les Nations Unies.",
                verdict="En faveur du plaignant.",
                date="2023-05-12",
                categories=[
                    Category(
                        name="Droit de l'immigration",
                        value=35,
                        children=[
                            ChildCategory(name="Politique de visa", value=20),
                            ChildCategory(name="Droit des réfugiés", value=15)
                        ]
                    ),
                    Category(
                        name="Droit financier",
                        value=45,
                        children=[
                            ChildCategory(name="Fiscalité", value=25),
                            ChildCategory(name="Droit des investissements", value=20)
                        ]
                    ),
                    Category(
                        name="Droit pénal",
                        value=20,
                        children=[
                            ChildCategory(name="Crimes en col blanc", value=10),
                            ChildCategory(name="Crimes violents", value=10)
                        ]
                    )
                ],
                categoryPercentages=[
                    CategoryPercentage(category="Droit de la concurrence", value=55),
                    CategoryPercentage(category="Droit des sociétés", value=30),
                    CategoryPercentage(category="Droit de la technologie", value=15)
                ],
                radarData=[
                    RadarData(category="Droit de la concurrence", value=80),
                    RadarData(category="Droit des sociétés", value=60),
                    RadarData(category="Droit de la technologie", value=50)
                ]
            ),
        ]

    else:
        return []


# POST endpoint for search and classification
@app.post("/search")
async def search(request: SearchRequest):

    text = request.query
    result = nlp_pipeline(text, law_categories)
    predicted_label = result["labels"][0]
    probabilities = dict(zip(result["labels"], result["scores"]))
    
    # Generate dummy court case data for now (this can be made dynamic based on the classification)
    return generate_court_cases(request.language)

# Root endpoint for health check
@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Case Classifier API!"}
