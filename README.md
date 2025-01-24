# BlackNews

1. Introduction
This document outlines the initial requirements and plan for the BlackNews application, an online platform designed to serve the black reading audience with relevant news, in-depth analysis, and interactive engagement. The application will utilize advanced AI agentic design patterns to automate content gathering, analysis, and user interaction, providing a personalized and informative experience.
2. Project Goals
Targeted Content: Focus on news, documents, and discussions relevant to the Black community.
Comprehensive Information: Collate diverse sources, including news, academic papers, and multimedia.
Interactive Experience: Enable users to ask questions, explore topics in depth, and customize their content feed.
AI-Driven Insights: Use AI to classify, summarize, and fact-check content, providing a more informed reading experience.
Admin Flexibility: Provide administrative tools to manage content sources and train the AI models.
3. Key Features
News Aggregation: Automated gathering of news from Black-oriented sources.
Document Repository: Storage and embedding of articles, academic papers, and other relevant documents.
AI-Powered Analysis:
Content embedding and semantic understanding.
Classification and summarization of news articles.
Prediction of article popularity.
Factual verification based on authoritative sources.


User Interaction:
Question answering based on content.
Personalized category and topic selection.
"Headlines of Note" section for important news.


Content Upload: Administrative interface for adding new documents and training data.
Multimedia Embedding Capture text from Audio and Video.
4. AI Agent Roles
The project will utilize AI agents with the following core roles:
News Gathering Agent:
Monitors specified Black-oriented news sources.
Downloads new articles, avoiding duplicates.
Tracks news location or region.


Content Embedding Agent:
Generates vector embeddings for all text content (news, documents, etc.) and multimedia.
Stores embeddings in the Supabase database.


Content Classification and Prediction Agent:
Classifies articles for popularity, topic, and other categories.
Predicts the popularity of new articles based on historical data and relevant articles


Fact-Checking Agent:
Verifies factual statements in articles against reliable sources (particularly academic and long form articles)


Multimedia Agent:
Captures text from audio and video sources
5. Technology Stack
Primary Language: Python
AI Models: Deepseek, Gemini (or similar models for embeddings, classification, summarization, etc.)
Database: Supabase (for storing articles, embeddings, user data, etc.)
Cloud Hosting: [To be determined - consider options like AWS, GCP, or DigitalOcean]
Other Tools: [To be determined - e.g., libraries for web scraping, NLP, vector databases, etc.]
