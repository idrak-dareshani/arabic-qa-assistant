from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from qa_engine import answer_question
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True, # Allows cookies to be sent
    allow_methods=["*"],  # Allows all methods (GET, POST, etc. as needed)
    allow_headers=["*"],  # Allows all headers
)

class Source(BaseModel):
    section_title: str
    level: str
    page: int

class QAAnswer(BaseModel):
    answer: str
    sources: List[Source]

@app.get("/qa", response_model=QAAnswer)
def get_qa(
    query: str = Query(...),
    level: Optional[str] = Query(None),
    section: Optional[str] = Query(None)
):
    filters = {}
    if level:
        filters['level'] = level.lower()
    if section:
        filters['section_title'] = section
    
    return answer_question(query, filters)
