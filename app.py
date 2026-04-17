"""
Story Forge - AI Content Generator (Streamlit App)
-------------------------------------------------

This application allows users to:
1. Fetch real-time information using Tavily (web search API)
2. Summarize that information using an LLM (OpenAI)
3. Generate engaging short-form video scripts (~200 words)
   suitable for Instagram Reels / YouTube Shorts

Tech Stack:
- Streamlit (UI)
- Tavily (real-time search)
- OpenAI (LLM for summarization + script generation)

Author: You 🚀
"""

import streamlit as st
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from openai import OpenAI

# -------------------------------
# LOAD ENV VARIABLES
# -------------------------------
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Initialize clients
client = OpenAI(api_key=openai_api_key)
tavily_client = TavilyClient(api_key=tavily_api_key)

# -------------------------------
# STREAMLIT CONFIG + DARK THEME
# -------------------------------
st.set_page_config(
    page_title="Story Forge",
    page_icon=":book:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom dark theme CSS
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    p, span, div { color: #d1d5db; }

    .stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
    }

    .stDownloadButton > button {
        background-color: #10b981;
        color: white;
        border-radius: 8px;
    }

    input, textarea {
        background-color: #1f2937 !important;
        color: white !important;
    }

    footer, #MainMenu { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# FUNCTION: GET REAL-TIME INFO
# -------------------------------
def get_realtime_info(query: str) -> str:
    """
    Fetches real-time information for a given query using Tavily
    and refines it using an LLM.

    Steps:
    1. Calls Tavily API to fetch search results
    2. Formats raw results into readable text
    3. Sends results to OpenAI model for summarization

    Args:
        query (str): User query/topic

    Returns:
        str: Clean, human-readable summarized information
             OR fallback message if no data found
    """

    try:
        summaries = []

        # Fetch results from Tavily
        resp = tavily_client.search(query, max_results=5, topic="general")

        if resp and resp.get("results"):
            for r in resp["results"]:
                title = r.get("title", "")
                url = r.get("url", "")
                snippet = r.get("snippet", "")

                summaries.append(f"{title}\n{snippet}")

            source_info = "\n\n".join(summaries)
        else:
            source_info = f"No relevant information found on {query}."

    except Exception as e:
        st.error(f"Error fetching real-time information: {e}")
        return None

    # LLM prompt for summarization
    prompt = f"""
You are a professional researcher and content creator.

Query:
{query}

Source Information:
{source_info}

Generate a clean, human-readable summary using ONLY the provided data.
Do not hallucinate or add external knowledge.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return source_info


# -------------------------------
# FUNCTION: GENERATE VIDEO SCRIPT
# -------------------------------
def generate_video_script(info_text: str) -> str:
    """
    Converts informational text into a creative short-form video script.

    The script is:
    - ~200 words
    - Engaging and emotional
    - Suitable for Instagram Reels / YouTube Shorts
    - Includes hook, message, and CTA

    Args:
        info_text (str): Input summarized content

    Returns:
        str: Generated video script OR error message
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a creative script writer for Instagram Reels and YouTube Shorts.
Generate an engaging 200-word script with a strong hook, storytelling, and CTA.
"""
                },
                {
                    "role": "user",
                    "content": f"info_text:\n{info_text}"
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        st.error(f"Error generating video script: {e}")
        return None


# -------------------------------
# MAIN UI FUNCTION
# -------------------------------
def main():
    """
    Main Streamlit UI logic.

    Flow:
    1. User enters a query
    2. Fetch real-time info
    3. Display summarized content
    4. Optionally generate video script
    5. Allow download of script
    """

    # Header
    st.markdown(
        "<h1 style='text-align: center; color: #4A90E2;'>Story Forge</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center;'>Create AI-powered stories and scripts instantly.</p>",
        unsafe_allow_html=True
    )

    # Input
    query = st.text_input("Enter your topic:")

    if query:
        with st.spinner("Fetching insights..."):
            info_text = get_realtime_info(query)

        if info_text:
            st.subheader("📊 Insights")
            st.write(info_text)

            # Ask user if script needed
            choice = st.radio(
                "Generate video script?",
                ("Yes", "No"),
                horizontal=True
            )

            if choice == "Yes":
                video_script = generate_video_script(info_text)

                if video_script:
                    st.subheader("🎬 Video Script")
                    st.write(video_script)

                    # Download button (safe)
                    st.download_button(
                        "Download Script",
                        data=video_script,
                        file_name=f"{query}_script.txt"
                    )
                else:
                    st.warning("Script generation failed.")
        else:
            st.warning("No data found. Try another query.")


# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    main()