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
- Add error handling and observability (logger)
- Add web crawler and scraper (beautiful soup)
- improve chunking strategy (document ingestion)
- Implement postgres for storing chat state persistently.
- Use gdrive API to store PDF and other set of documents
- Implement streaming and complete langgraph full implementation - additional LG 
- Create API - FastAPI
- Create UI - Streamlit
- model re-training (q-lora, lora)
- Update README
- Deploy on cloud ()
- Add tests
- Improve prompts
- Evaluation (data science eval methods)

## Imprevements Neede
1- improve chunk size , not too small as docling creates.
2- Still need to implement that to create ids, metadata only when the embedding is created. Otherwise mismatch during upserting. due to empty string embedding was not getting created and wrong api resp was getting received

## Imprevements made
1- cleaning the data before even adding into json data from docling, earlier use to clean after creating the json out of docling doc.
2- Added logging mechanism for data pre-processes
3- dataset builder can accept both file and a disct obj of content of document
4- API created to upload document on local via uvicorn api


#Save libraries used
pipreqs . \
  --force \
  --ignore venv311 \
  --savepath requirements-min.txt