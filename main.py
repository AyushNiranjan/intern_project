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
import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

