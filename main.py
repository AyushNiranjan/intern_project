from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_lead_data

app = FastAPI()  # ← THIS must be here!

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_lead_info")
def get_lead_info(company: str = Query(...)):
    try:
        result = get_lead_data(company)
        return result
    except Exception as e:
        return {"error": str(e)}
