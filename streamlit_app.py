import streamlit as st
import os
from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# List of specific barrier types without categorization
BARRIER_TYPES = [
    "lack-of-work-experience",
    "lack-of-technical-skills",
    "lack-of-soft-skills",
    "insufficient-qualifications",
    "literacy-issues",
    "numeracy-issues",
    "physical-disability",
    "chronic-illness",
    "mental-health-issues",
    "substance-abuse",
    "caring-responsibilities",
    "lack-of-stable-housing",
    "financial-instability",
    "lack-of-transportation",
    "job-location-accessibility",
    "limited-access-to-technology",
    "age-discrimination",
    "racial-discrimination",
    "gender-discrimination",
    "criminal-record-discrimination",
    "low-self-esteem",
    "lack-of-motivation",
    "poor-work-habits",
    "economic-downturn",
    "lack-of-job-availability",
    "social-isolation",
    "lack-of-support-network",
    "language-barriers",
    "immigration-status",
    "criminal-background",
    "benefits-system-complexity",
    "limited-digital-literacy",
    "no-computer-access",
    "no-internet-access",
    "personal-relationships",
    "money-management",
    "debt",
    "ongoing-criminal-proceedings",
    "neurodiversity-learning-difficulties",
    "cv-issues",
    "job-search-skills",
    "job-application-skills",
    "interview-skills",
    "lack-of-job-goals-or-interest"
]

def identify_barriers(conversation):
    barrier_types_str = ", ".join([f"'{b}'" for b in BARRIER_TYPES])
    
    system_prompt = f"""
    You are an AI assistant specialized in identifying barriers to employment from conversations between an employment support coach and a program participant. Analyze the given conversation and identify the main barriers or challenges the participant is facing.

    Only use the following predefined barrier types: {barrier_types_str}

    Output your analysis as a JSON object with a 'barriers' key containing an array of barrier objects. Each barrier object should have a 'tag' (one of the predefined types) and a 'reason' (a brief explanation).

    Example output format:
    {{
        "barriers": [
            {{"tag": "lack-of-work-experience", "reason": "Participant mentions limited work history"}},
            {{"tag": "lack-of-technical-skills", "reason": "Struggles with latest design software"}},
            {{"tag": "mental-health-issues", "reason": "Mentions having anxiety affecting focus and motivation"}}
        ]
    }}

    Only include barriers that are explicitly mentioned or strongly implied in the conversation. Do not infer barriers without clear evidence from the text. If no barriers from the predefined list are identified, return an empty array.
    """

    user_prompt = f"Analyze the following text and output a list of the main barriers to employment from the predefined list, in the specified JSON format:\n\n{conversation}"

    parameters = {
        "model": "gpt-4o",
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        response = client.chat.completions.create(**parameters)
        barriers_json = response.choices[0].message.content.strip()
        barriers = json.loads(barriers_json)
        return barriers.get("barriers", [])
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

def main():
    st.title("Earlybird Barrier Identifier")

    # Text area for conversation input
    conversation = st.text_area("Paste the conversation here:", height=300)

    # Process button
    if st.button("Identify Barriers"):
        if conversation:
            with st.spinner("Analyzing conversation..."):
                barriers = identify_barriers(conversation)

            # Display results
            if barriers:
                st.subheader("Identified Barriers:")
                for barrier in barriers:
                    st.markdown(f"**{barrier['tag']}:** {barrier['reason']}")
            else:
                st.info("No barriers from the predefined list were identified in the conversation.")
        else:
            st.warning("Please enter a conversation to analyze.")

    # Display the list of possible barrier types
    with st.expander("View all possible barrier types"):
        st.write(", ".join(BARRIER_TYPES))

if __name__ == "__main__":
    main()