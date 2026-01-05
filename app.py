import streamlit as st
from openai import OpenAI

# PASTE YOUR API KEY BETWEEN THE QUOTES BELOW
API_KEY = "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"

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Cost-Effectiveness Summarizer",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("Cost-Effectiveness Plain Language Summarizer")
st.write("Transform technical health economics outputs into clear, audience-appropriate summaries.")

# Create two columns for input
col1, col2 = st.columns([2, 1])

with col1:
    he_results = st.text_area(
        "Paste your health economics results here:",
        height=300,
        placeholder="Example: Base case ICER: $45,000 per QALY gained..."
    )

with col2:
    st.write("### Select Target Audience")
    audience = st.selectbox(
        "Who is this summary for?",
        options=[
            "Executive Leadership",
            "Payer/Formulary Committee",
            "Clinical Team",
            "HTA Submission Reviewer",
            "Patient Advocacy Group"
        ]
    )

    if audience == "Executive Leadership":
        st.info("Focus on strategic implications and bottom-line recommendations.")
    elif audience == "Payer/Formulary Committee":
        st.info("Emphasize budget impact and cost-effectiveness thresholds.")
    elif audience == "Clinical Team":
        st.info("Highlight patient outcomes and clinical meaningfulness.")
    elif audience == "HTA Submission Reviewer":
        st.info("Stress methodological robustness and uncertainty handling.")
    else:
        st.info("Explain results in accessible terms focused on quality of life.")

    additional_context = st.text_area(
        "Additional context (optional):",
        height=100,
        placeholder="E.g., therapeutic area, comparator..."
    )

if st.button("Generate Summary", type="primary", use_container_width=True):

    if not he_results.strip():
        st.warning("Please paste your health economics results first.")
    else:
        if audience == "Executive Leadership":
            audience_instruction = "You are translating health economics results for C-suite executives. Focus on clear recommendations, strategic implications, key risks, and bottom-line budget figures. Avoid jargon. Lead with the recommendation. Be concise and decisive."
        elif audience == "Payer/Formulary Committee":
            audience_instruction = "You are translating health economics results for a pharmacy and therapeutics committee. Focus on cost-effectiveness relative to standard thresholds ($50K, $100K, $150K per QALY), budget impact over 1-5 years, uncertainty drivers, and comparison to formulary alternatives."
        elif audience == "Clinical Team":
            audience_instruction = "You are translating health economics results for physicians and clinical staff. Focus on what QALY gains mean for patients (symptoms, function, survival), clinical meaningfulness, and patient selection considerations. Connect the numbers to patient care."
        elif audience == "HTA Submission Reviewer":
            audience_instruction = "You are preparing a summary for an HTA agency reviewer like NICE or ICER. Focus on methodological approach, handling of uncertainty (PSA, scenarios), key limitations, and robustness of the base case. Be precise and technical."
        else:
            audience_instruction = "You are explaining health economics results to patient advocates. Focus on what the treatment means for quality of life, why cost matters for access, and what uncertainty means for individual patients. Avoid all jargon. Use everyday language."

        context_text = ""
        if additional_context.strip():
            context_text = "Additional context: " + additional_context

        full_prompt = audience_instruction + "\n\nHEALTH ECONOMICS RESULTS TO SUMMARIZE:\n" + he_results + "\n\n" + context_text + "\n\nProvide a clear, well-structured summary in 2-4 paragraphs. Start with the most important takeaway for this audience."

        with st.spinner("Generating summary..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": full_prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )

                summary = response.choices[0].message.content

                st.write("---")
                st.write("### Summary for " + audience)
                st.write(summary)

                st.write("---")
                st.download_button(
                    label="Download Summary as Text File",
                    data=summary,
                    file_name="ce_summary.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error("Error generating summary: " + str(e))

st.write("---")
st.caption("This tool uses AI to translate technical health economics outputs. Always verify summaries against source data.")

