📖 Story Forge

Story Forge is an AI-powered content generation system that transforms real-time information into human-like insights and engaging short-form video scripts for platforms like Instagram Reels and YouTube Shorts.

It combines:

🌐 Real-time web search (Tavily)
🧠 LLM-powered research & summarization
🎬 Creative script generation
🔌 MCP (Model Context Protocol) tool integration
🎨 Streamlit UI for interactive usage



🚀 Use Case

In today’s content-driven world, creators struggle to:

Find reliable, up-to-date information
Convert raw data into engaging content
Maintain consistency and creativity at scale

Story Forge solves this by:

Fetching real-time information based on a topic
Converting it into clear, human-readable insights
Generating high-quality short video scripts (~200 words)
Enabling both:
UI-based usage (Streamlit)
Tool-based usage (MCP server)

This makes it ideal for:

🎥 Content creators
📱 Social media managers
📰 News summarization
📊 Quick research + storytelling workflows



⚙️ Features
🔎 Real-Time Information Retrieval
Uses Tavily API to fetch latest data
Aggregates multiple sources
🧠 AI Research Assistant
Converts raw data into:
Structured insights
Clean summaries
Trend analysis
🎬 Video Script Generator
Generates:
Hook-based scripts
Emotional + engaging storytelling
~200 word short-form content
🔌 MCP Integration

Exposes tools like:

get_latest_info_mcp
generate_video_script_mcp

These can be used by:

AI agents
Multi-agent systems
External MCP clients


▶️ How to Run Streamlit 
uv run streamlit run app.py

▶️ How to Run mcpserver
uv run mcp_server.py



