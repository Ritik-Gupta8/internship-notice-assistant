import streamlit as st
from google.adk.agents import Agent
from google.adk.runners import Runner
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create Agent
agent = Agent(
    model="gemini-2.5-flash",
    name="Internship_Assistant",
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

notice_text = st.text_area("Paste the Internship/Placement Notice here:", height=200)

import asyncio
from google.adk.runners import Runner

if st.button("Generate Action Plan"):
    if notice_text:
        with st.spinner("Agent is analyzing..."):
            from google.adk.sessions.in_memory_session_service import InMemorySessionService

            session_service = InMemorySessionService()
            runner = Runner(
                agent=agent,
                app_name="internship-assistant",
                session_service=session_service,
                auto_create_session=True
            )

            # run_debug evaluates the message and returns the collected events asynchronously
            try:
                events = asyncio.run(
                    runner.run_debug(notice_text, quiet=True)
                )

                # extract the text from the last event
                response = events[-1].output_text if hasattr(events[-1], 'output_text') else events[-1].text

                st.markdown("---")
                st.markdown(response)
            except Exception as e:
                st.error(f"⚠️ Failed to generate action plan. The API may be experiencing high demand (Error: {e}). Please try again later.")
    else:
        st.warning("Please paste a notice first!")