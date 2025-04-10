# 🚀 AI-Powered Lead Generation & CEO Email Finder Tool

An end-to-end AI-powered scraping system that extracts **CEO names, emails, company descriptions, and LinkedIn profiles** for any company entered in a **Google Sheet**.

This tool merges the power of **LLMs (Groq + LLaMA-3)**, **search APIs**, **web scraping**, and **email verification** into a single pipeline. Ideal for B2B marketers, startup founders, VCs, and recruiters.

---

## 📊 Use Cases

This project is designed for:
- 🔍 **B2B marketers** doing outreach campaigns
- 💼 **Founders or VCs** doing competitive research
- 📈 **Lead generation teams** needing clean decision-maker data
- 🤖 Anyone tired of expensive tools like ZoomInfo or Apollo

---

## 🧠 Architecture Overview


---

## 🛠️ Tech Stack

| Layer       | Tech                             | Purpose                                       |
|------------|----------------------------------|-----------------------------------------------|
| 🔍 Search   | [Serper.dev](https://serper.dev) | Google Search API for top results             |
| 🧠 LLM      | LLaMA-3 via [Groq](https://console.groq.com) | Reasoning to identify the CEO                |
| 📚 RAG      | LangChain + FAISS                | Contextual understanding for CEO name         |
| 🔎 Scraping | BeautifulSoup + requests         | Extract LinkedIn, About, Titles, etc.         |
| 📬 Email    | Email Pattern Generator + [NeverBounce](https://neverbounce.com) | Verify deliverable emails                    |
| 🌐 Backend  | FastAPI                          | API endpoint for communication with Sheets    |
| 📄 Frontend | Google Sheets + Apps Script      | Easy-to-use frontend for non-technical users  |
| 🚀 Hosting  | Ngrok (dev) / Render (prod)      | Tunnels or deploys backend                    |

---

## 🔐 Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
NEVERBOUNCE_API_KEY=your_neverbounce_api_key
