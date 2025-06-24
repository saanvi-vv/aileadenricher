# 🚀 AI-Powered Lead Enrichment Agent

This project is a Streamlit-based web application that allows RevOps teams, startup founders, and growth strategists to automatically extract and enrich data about SaaS companies using cutting-edge AI. It combines [Firecrawl](https://firecrawl.dev/) for content extraction and [Gemini 2.0 Flash](https://ai.google.dev/) for language understanding to generate high-quality summaries of what each company does — all without writing a single prompt or scraping content manually.

TRY IT OUT AT: https://lead-enricher.streamlit.app/
---

## 🧩 Why This Project

Revenue Operations (RevOps) teams often spend hours researching leads manually, copying/pasting company data into sheets, and summarizing company offerings for sales enablement. This project automates that pain entirely.

### Built for:
- RevOps Analysts & SDRs
- B2B SaaS growth teams
- AI and automation enthusiasts building intelligent agents

---

## ✨ Features

- 🔎 **Extract Website Content**: Uses Firecrawl to pull structured homepage text and metadata.
- 🧠 **Summarize with Gemini Flash**: Leverages Gemini 2.0 Flash to create insightful, human-like company descriptions.
- 📊 **Instant Lead Table**: See enriched results in a clear Streamlit DataFrame.
- 📥 **Export to CSV**: Download your leads with a single click.
- 🧠 **Gemini Prompt Engineering** (under the hood): Uses clear, focused prompts for generating business-specific summaries.

---

## 🧠 Prompt Strategy

We use Gemini 2.0 Flash with dynamic prompts based on user-selected tone. Example:

> "Summarize what this SaaS company does in a **conversational** tone based on the following homepage content..."


---

## 🛠️ Tech Stack

| Layer           | Tool / Framework                      |
|----------------|----------------------------------------|
| Language Model | Gemini 2.0 Flash (Google Generative AI)|
| Data Extractor | Firecrawl.dev API                      |
| Frontend       | Streamlit (Python)                     |
| Data Handling  | Pandas                                 |

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/lead-enrichment-agent.git
cd lead-enrichment-agent
(remember to download required libraries using 'pip install -r requirements.txt')
