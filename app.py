import streamlit as st
from google.adk.agents import Agent
import os

# Set up the Agent
agent = Agent(
    model="gemini-1.5-flash",
    name="Internship-Assistant",
    instruction="""You are an expert career coach. 
    Analyze the provided internship/job notice. 
    Return a structured response: 
    1. Summary (Company, Role, Deadline)
    2. Eligibility Criteria
    3. Required Documents
    4. A 'Ready-to-Send' Application Email draft.
    Use Markdown formatting with bold headers."""
)

st.title("🎓 Internship Notice Assistant")
st.write("Turn messy placement notices into action plans instantly.")

# User Input
notice_text = st.text_area("Paste the Internship/Placement Notice here:", height=200)

if st.button("Generate Action Plan"):
    if notice_text:
        with st.spinner("Agent is analyzing..."):
            # Call the ADK Agent
            response = agent.ask(notice_text)
            st.markdown("---")
            st.markdown(response)
    else:
        st.warning("Please paste a notice first!")