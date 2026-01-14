LegalAI - Legal AI Assistant

This application helps advocates to perform various activities of their day to day tasks at a lightening fast speed.
For example, legal research, creation of legal documents, etc

## What this project is
LegalAI solves the issue of hallucination in the AI usage that usually is done by legal professionals. Where they are not highly technically equipped to right and verify detailed prompts and its response.
LegalAI solves this by using Agentic RAG system that provides solution only from a real source.

## Current status
- Initial version (v0.1)
- Work in progress
- APIs and UI not developed yet

## Tech stack
- Python
- LangGraph
- Langchain
- Euri 
- Chroma DB

## How to run (basic)
1. Clone the repo
2. create an .env file with API key for the LLM
3. Install dependencies
4. Run main entry file

## Folder structure (high level)
- 

## Future plans
- Add error handling and observability
- Create API
- Create UI
- Deploy on cloud
- Add tests
- Improve prompts

#Save libraries used
pipreqs . \
  --force \
  --ignore venv311 \
  --savepath requirements-min.txt