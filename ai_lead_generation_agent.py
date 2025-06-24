import streamlit as st
import pandas as pd
import google.generativeai as genai
from firecrawl import FirecrawlApp
import os

# --- Streamlit UI ---
st.title("🚀 AI-Powered Lead Enrichment Agent")
st.write("Enter SaaS company websites. We'll extract homepage content and summarize what each company does using Gemini.")

with st.sidebar:
    st.header("enter api keys:")
    st.write("You can get your API keys from the respective platforms.")
    FIRECRAWL_API_KEY = st.text_input("Firecrawl API Key", type="password")
    GEMINI_API_KEY = st.text_input("Gemini API Key", type="password")


urls_input = st.text_area("Enter website URLs (one per line)")
run_button = st.button("Enrich Leads")

if run_button and urls_input and FIRECRAWL_API_KEY and GEMINI_API_KEY:
    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    # Set up Firecrawl
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
                        "prompt": "Extract the homepage content of this SaaS company.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string"}
                            },
                            "required": ["content"]
                        }
                    }
                )

                # Access the content from the response object
                content = response.extract["content"]

                # Summarize with Gemini
                prompt = f"Summarize what this SaaS company does based on the following homepage content:\n\n{content}"
                summary = model.generate_content(prompt).text.strip()

                results.append({"Website": url, "Summary": summary})
            except Exception as e:
                results.append({"Website": url, "Summary": f"Error: {e}"})

    df = pd.DataFrame(results)
    st.success("✅ Enrichment complete!")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "enriched_leads.csv", "text/csv")