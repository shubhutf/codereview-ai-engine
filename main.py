from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.pr_pipeline import pr_pipeline

app = FastAPI()


class PRRequest(BaseModel):
    pr_url: str



@app.post("/analyze")
def analyze_pr(body: PRRequest):
    try:
        report = pr_pipeline(body.pr_url)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/")
def health_check():
    return {"status": "ok"}