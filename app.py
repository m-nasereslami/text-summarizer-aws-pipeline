from fastapi import FastAPI
from pydantic import BaseModel
from summarizer import summarize_text

app = FastAPI()

class SummarizeRequest(BaseModel):
    text: str

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    summary = summarize_text(req.text)
    return {"summary": summary}
