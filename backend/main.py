from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from qa_engine import answer_question

app = FastAPI()

class Source(BaseModel):
    section_title: str
    level: str
    page: int

class QAAnswer(BaseModel):
    answer: str
    sources: List[Source]

@app.get("/qa", response_model=QAAnswer)
def get_qa(query: str = Query(...)):
    return answer_question(query)
