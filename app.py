import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="CE Summarizer", page_icon="📊", layout="wide")
st.title("Cost-Effectiveness Plain Language Summarizer")
st.write("Transform technical health economics outputs into clear summaries.")

col1, col2 = st.columns([2, 1])

with col1:
    he_results = st.text_area("Paste your health economics results here:", height=300)

with col2:
    st.write("### Select Target Audience")
    audience = st.selectbox("Who is this summary for?", ["Executive Leadership", "Payer/Formulary Committee", "Clinical Team", "HTA Submission Reviewer", "Patient Advocacy Group"])
    additional_context = st.text_area("Additional context (optional):", height=100)

if st.button("Generate Summary", type="primary", use_container_width=True):
    if not he_results.strip():
        st.warning("Please paste your health economics results first.")
    else:
        if audience == "Executive Leadership":
            instruction = "Translate for C-suite executives. Focus on recommendations, strategic implications, risks, and budget. Avoid jargon. Be concise."
        elif audience == "Payer/Formulary Committee":
            instruction = "Translate for a P&T committee. Focus on cost-effectiveness vs thresholds, budget impact, uncertainty, and formulary comparison."
        elif audience == "Clinical Team":
            instruction = "Translate for physicians. Focus on what QALYs mean for patients, clinical meaningfulness, and patient selection."
        elif audience == "HTA Submission Reviewer":
            instruction = "Translate for an HTA reviewer. Focus on methodology, uncertainty handling, limitations, and robustness."
        else:
            instruction = "Translate for patient advocates. Focus on quality of life impact, why cost matters for access, in everyday language."

        prompt = instruction + "\n\nRESULTS:\n" + he_results
        if additional_context.strip():
            prompt = prompt + "\n\nCONTEXT: " + additional_context
        prompt = prompt + "\n\nProvide a 2-4 paragraph summary."

        with st.spinner("Generating..."):
            try:
                response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], max_tokens=1000)
                summary = response.choices[0].message.content
                st.write("---")
                st.write("### Summary for " + audience)
                st.write(summary)
            except Exception as e:
                st.error("Error: " + str(e))
```

5. **Make sure there's nothing after the last line** (`st.error("Error: " + str(e))`)

6. Click **"Commit changes"**

7. Click **"Commit changes"** again

---

## **Then Check Streamlit Secrets**

1. Go to share.streamlit.io

2. Click on your app → **Settings** → **Secrets**

3. Make sure it contains:
```
   OPENAI_API_KEY = "sk-proj-your-actual-new-key"
