\# Offline RAG + Gemma Integration



This folder validates the end-to-end integration between local

educational content retrieval and the local Gemma model.



\## Pipeline



Student Question

↓

Retrieval

↓

Relevant Educational Content

↓

Grounded Teaching Prompt

↓

Local Gemma

↓

Teaching Response + Source Metadata



\## Components



\### retrieval\_service.py



Provides a service layer around the previously validated local

FAISS retrieval pipeline.



\### prompt\_builder.py



Builds a grounded teaching prompt using:



\- Student question

\- Student level

\- Retrieved educational content

\- Source metadata



The prompt instructs Gemma to use retrieved content as its primary

knowledge source and avoid unsupported information.



\### gemma\_client.py



Provides an integration adapter around the previously validated

local Gemma client.



The model runs through Ollama using:



gemma3:1b



No cloud API is required.



\### rag\_gemma\_pipeline.py



Connects retrieval, prompt construction, and Gemma into one

end-to-end pipeline.



\### test\_integration.py



Tests the complete pipeline and verifies:



1\. Relevant content is retrieved.

2\. Retrieved content reaches the integration.

3\. A grounded teaching prompt is generated.

4\. Gemma produces a response.

5\. Source metadata is returned.

6\. The pipeline operates using local components.



\## Offline Architecture



The integration is designed to work without cloud services.



Local components:



\- Sentence Transformers

\- FAISS

\- Ollama

\- Gemma 3:1b



\## Running the Test



From the repository root:



```powershell

python .\\offline-rag-gemma-integration\\test\_integration.py

