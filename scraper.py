from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.chains import RetrievalQA
import requests
import re
import os

# === CONFIG ===
llm = ChatGroq(
    model_name="llama3-8b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY", "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")
)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
serper_api_key = os.getenv("SERPER_API_KEY", "d5893ef70ad716f59de244976a281c24d4a89e2c")
neverbounce_api_key = os.getenv("NEVERBOUNCE_API_KEY", "private_b29bbe907d639c538fc78f02f22a8b9a")
SERPER_URL = "https://google.serper.dev/search"

# === SEARCH GOOGLE ===
def search_google(query):
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(SERPER_URL, json={"q": query}, headers=headers)
    return response.json()

# === SCRAPE CONTENT ===
def scrape_content(company):
    query = f"{company} CEO name"
    results = search_google(query)
    urls = [res["link"] for res in results.get("organic", [])[:10]]

    print(f"🔗 Found {len(urls)} URLs to scrape.")
    loaders = [WebBaseLoader(url) for url in urls]
    data = []
    for loader in loaders:
        try:
            data.extend(loader.load())
            print(f"✅ Loaded: {loader.web_path}")
        except Exception as e:
            print(f"❌ Error loading {loader.web_path}: {e}")
    return data

# === CREATE VECTORSTORE ===
def create_vectorstore(data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=384, chunk_overlap=50)
    chunks = text_splitter.split_documents(data)
    docs = [text if isinstance(text, Document) else Document(page_content=text) for text in chunks]
    return FAISS.from_documents(docs, embedding_model)

# === EXTRACT CEO NAME ===
def get_ceo_name(vectorstore):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True
    )
    response = qa_chain.invoke("Who is the CEO of the company?")
    answer_text = response["result"]
    print("🧠 LLM Answer:", answer_text)

    if not answer_text or "not found" in answer_text.lower():
        return "Not Found"

    match = re.search(r"(?:CEO.*?is\s)?([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", answer_text)
    return match.group(1).strip() if match else answer_text.strip()

# === GET DOMAIN FROM COMPANY NAME ===
def get_domain_from_company(company_name):
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    payload = {"q": f"{company_name} official site"}
    resp = requests.post(SERPER_URL, headers=headers, json=payload)
    results = resp.json()
    first_link = results.get("organic", [{}])[0].get("link", "")
    domain = first_link.split("//")[-1].split("/")[0]
    return domain

# === GENERATE POSSIBLE EMAILS ===
def generate_possible_emails(full_name, domain):
    full_name = full_name.lower().strip()
    domain = domain.lower().strip()
    parts = full_name.split()
    if len(parts) < 2:
        return []

    first = parts[0]
    last = parts[-1]
    first_initial = first[0]
    last_initial = last[0]

    patterns = [
        f"{first}@{domain}",
        f"{first}.{last}@{domain}",
        f"{first}{last}@{domain}",
        f"{first}_{last}@{domain}",
        f"{first}{last_initial}@{domain}",
        f"{first_initial}{last}@{domain}",
        f"{first_initial}.{last}@{domain}",
        f"{first}.{last_initial}@{domain}",
        f"{last}@{domain}",
        f"{first}-{last}@{domain}",
        f"{first_initial}{last_initial}@{domain}",
        f"ceo@{domain}",
        f"founder@{domain}",
        f"{first}.{last}@email.{domain}",
    ]

    return list(set(patterns))

# === VALIDATE EMAIL WITH SCORE ===
def validate_email_with_score(email):
    url = "https://api.neverbounce.com/v4/single/check"
    params = {
        "key": neverbounce_api_key,
        "email": email,
    }
    response = requests.get(url, params=params)
    result = response.json()
    status = result.get("result")

    score_map = {
        "valid": 3,
        "unknown": 2,
        "catchall": 2,
        "disposable": 1,
        "invalid": 0
    }

    return {
        "email": email,
        "status": status,
        "score": score_map.get(status, 0)
    }

# === GET TOP EMAILS ===
def get_top_emails(emails, top_n=3):
    results = [validate_email_with_score(email) for email in emails]
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    return sorted_results[:top_n]

# === LINKEDIN & DESCRIPTION ===
def get_linkedin_profile(name, company):
    query = f"site:linkedin.com/in {name} {company}"
    data = search_google(query)
    for result in data.get("organic", []):
        if "linkedin.com/in" in result["link"]:
            return result["link"]
    return "Not found"

def get_company_linkedin(company):
    query = f"{company} LinkedIn site:linkedin.com/company"
    data = search_google(query)
    for result in data.get("organic", []):
        if "linkedin.com/company" in result["link"]:
            return result["link"]
    return "Not found"

def get_company_description(company_name, api_key):
    url = SERPER_URL
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {"q": f"What does {company_name} do?"}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            return data['organic'][0]['snippet']
        except (KeyError, IndexError):
            return "No description found."
    else:
        return f"Error: {response.status_code} - {response.text}"

# === MAIN FUNCTION ===
def get_lead_data(company):
    print(f"\n🔍 Searching for: {company}")
    data = scrape_content(company)
    description = get_company_description(company, serper_api_key)

    if not data:
        print("⚠️ No data found.")
        return {
            "company": company,
            "ceo_name": "Not found",
            "ceo_email": [],
            "ceo_linkedin": "Not found",
            "company_linkedin": get_company_linkedin(company),
            "description": description
        }

    vectorstore = create_vectorstore(data)
    ceo_name = get_ceo_name(vectorstore)
    ceo_linkedin = get_linkedin_profile(ceo_name, company) if ceo_name != "Not Found" else "Not found"
    company_linkedin = get_company_linkedin(company)

    domain = get_domain_from_company(company)
    possible_emails = generate_possible_emails(ceo_name, domain) if ceo_name != "Not Found" else []
    top_emails = get_top_emails(possible_emails)

    return {
        "company": company,
        "ceo_name": ceo_name,
        "ceo_email": top_emails,
        "ceo_linkedin": ceo_linkedin,
        "company_linkedin": company_linkedin,
        "description": description
    }

# === CLI ENTRYPOINT (safe for Railway) ===
def cli():
    company = input("Enter company name: ").strip()
    result = get_lead_data(company)
    print("\n📊 Lead Data:")
    for key, value in result.items():
        print(f"{key}: {value}")

# === SAFE ENTRYPOINT ===
if __name__ == "__main__":
    import sys
    import multiprocessing
    multiprocessing.set_start_method("spawn", force=True)

    if "cli" in sys.argv:
        cli()
