import streamlit as st
import pandas as pd
import google.generativeai as genai
from firecrawl import FirecrawlApp
import os

st.title("🚀 AI-Powered Lead Enrichment Agent")
st.write("Enter company websites. We'll extract homepage content and summarize what each company does using Gemini.")
st.badge("Psst... the secret controls are hiding in the sidebar 👀")

with st.sidebar:
    st.markdown("---")
    tone = st.selectbox(
    "🗣️ Choose summary tone",
    ["Concise", "Conversational", "Salesy", "Technical"],
    index=0
    )
    st.markdown("---")
    st.markdown("### 📬 Contact Me")
    st.markdown("[GitHub](https://github.com/justrohan29)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/rohnis/)")
    st.markdown("[📄 Download Resume](https://flowcv.com/resume/8q83wa073v)", unsafe_allow_html=True)
FIRECRAWL_API_KEY = st.secrets["FIRECRAWL_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]



urls_input = st.text_area("Enter website URLs (one per line)")
run_button = st.button("Enrich Leads")

if run_button and urls_input and FIRECRAWL_API_KEY and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

    urls = [u.strip() for u in urls_input.splitlines() if u.strip()]
    results = []

    with st.spinner("Extracting and summarizing..."):
        for url in urls:
            try:
                response = firecrawl.scrape_url(
                    url=url,
                    formats=["extract"],
                    extract={
                        "prompt": """You are extracting homepage content from a company website that may belong to sectors like manufacturing, energy, infrastructure, metals, or cement. 
                                        Extract all textual content from the homepage that explains:
                                        - What the company does
                                        - Its product or service offerings
                                        - Industries served
                                        - Technologies or processes used
                                        - Sustainability or innovation highlights
                                        - Any major clients, projects, or markets mentioned

                                        Ensure the extracted content is clean and complete, ignoring navigation bars, cookie banners, and footers.""",

                        "schema": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string"}
                            },
                            "required": ["content"]
                        }
                    }
                )

                content = response.extract["content"]

                prompt = f"""
You are an expert B2B company analyst. Based on the extracted homepage content below, summarize what this company does. 
The company is **not SaaS** — it may belong to industries like metals, infrastructure, energy, cement, or heavy manufacturing.

Generate the summary in a **{tone.lower()}** tone and include as much detail as possible.

Respond in the following format:

**Company Overview**: What does the company do?
**Key Offerings**: List major products, services, or capabilities.
**Industries Served**: Which sectors or markets do they cater to?
**Technologies or Expertise**: Highlight any advanced processes, R&D, or innovations.
**Strategic Edge**: What makes this company unique?
**Sustainability/CSR**: Mention any sustainability or impact initiatives if stated.

Homepage content:
                {content}
                """
                summary = model.generate_content(prompt).text.strip()

                results.append({"Website": url, "Summary": summary})
            except Exception as e:
                results.append({"Website": url, "Summary": f"Error: {e}"})

    df = pd.DataFrame(results)
    st.success("✅ Enrichment complete!")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "enriched_leads.csv", "text/csv")
