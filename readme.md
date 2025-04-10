# 🚀 AI-Powered Lead Generation & CEO Email Finder Tool

An end-to-end AI-powered scraping tool that extracts **CEO name, emails, company description, and LinkedIn profiles** for any company entered in a **Google Sheet**.

This tool combines:
- **LLMs (Groq + LLaMA-3)** for CEO name reasoning
- **Web scraping + search results**
- **Email generation & validation**
- **FastAPI backend**
- **Google Sheets Apps Script** for a smooth frontend UX

---

## 📊 Use Case

This project is designed for:
- B2B marketers doing outreach
- Founders/VCs doing market scans
- Lead generation analysts
- Anyone trying to find accurate **decision-maker info** fast

---

## 🧠 How It Works (Architecture)


---

## 🛠️ Tech Stack

| Layer       | Tech                             |
|------------|----------------------------------|
| 🔍 Search   | [Serper.dev](https://serper.dev) |
| 🧠 LLM      | LLaMA-3 via [Groq](https://console.groq.com) |
| 📚 RAG      | LangChain + FAISS                |
| 🔎 Scraping | BeautifulSoup + requests         |
| 📬 Email    | NeverBounce                      |
| 🌐 Backend  | FastAPI                          |
| 📄 Frontend | Google Sheets + Apps Script      |
| 🚀 Hosting  | Ngrok                            |

---

## 🔑 API Keys Setup

Create a `.env` file at the root of the project:

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
NEVERBOUNCE_API_KEY=your_neverbounce_api_key
