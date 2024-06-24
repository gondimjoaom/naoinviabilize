# RAG on Não Inviabilize podcast transcriptions

## RAG Pipeline

### 1. Data Webcrawling

Extract episodes transcriptions from Não Inviabilize podcast website.

### 2. QA synthetization

**LLaMA 3 70B**: generate questions and answers based on transcriptions.

### 3. Multi-index pre-processing

Chunknize episodes transcriptions:
- Window of sentences splitter
- ...

### 4. Retrieval of passages

1. BM25 vs Semantic Embeddings
2. MonoPTT5 Reranking

### 5. Generation

1. Naive approach
2. Agentic approach (ReAct, ...)

### 6. Pipeline evaluation

RAGAs:
- Faithfulness Score
- Answer Relevance
- Context Relevancy
