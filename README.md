# Omnichannel RAG Chatbot

## Overview

Omnichannel RAG Chatbot is an AI-powered customer support and lead generation platform that provides a unified experience across both Website and WhatsApp channels.

The system uses a shared knowledge base, collects customer enquiries, stores leads, and answers questions using company information, FAQs, website content, and uploaded documents.

Designed to be reusable across organizations by simply changing the knowledge source, prompts, and configuration.

---

## Screenshots

### Website Chatbot

Demonstrates lead collection, knowledge retrieval, source attribution, and AI-powered responses.

![Website Chatbot](screenshots/website-chatbot.png)

---

### WhatsApp Chatbot

Demonstrates customer interaction through WhatsApp using the same shared knowledge base.

![WhatsApp Chatbot](screenshots/whatsapp-chatbot.png)

---

## Features

### Website Chatbot

* Collects customer Name, Email, and Phone Number
* Stores lead information in PostgreSQL
* Answers questions using company knowledge
* Maintains conversation history
* Displays source references used for responses

### WhatsApp Chatbot

* Uses the same knowledge base as the website chatbot
* Collects customer information through WhatsApp conversations
* Stores customer leads and chat history
* Automatically answers company and service-related questions
* Prevents duplicate message processing

### Shared Knowledge Base

* Website content ingestion
* FAQ ingestion
* PDF and document ingestion
* Qdrant vector search
* Hybrid retrieval architecture
* Cross-encoder reranking

---

## Architecture

User
↓
Website Chat / WhatsApp Chat
↓
FastAPI Backend
↓
Lead Collection & Session Management
↓
Hybrid Retrieval Pipeline

* Dense Retrieval (BGE Embeddings + Qdrant)
* BM25 Keyword Retrieval
* Reciprocal Rank Fusion (RRF)
* CrossEncoder Reranker

↓
Llama 3.2
↓
Response Generation

---

## Retrieval Strategy

The project focuses on improving both Recall and Precision.

### Recall Improvements

* Dense Vector Retrieval
* BM25 Keyword Retrieval
* Reciprocal Rank Fusion (RRF)

These stages maximize the chances of retrieving all relevant information.

### Precision Improvements

* CrossEncoder Reranker

The reranker re-scores retrieved chunks and selects the most relevant context before passing it to the LLM.

In simple terms:

* High Recall → Don't miss important information.
* High Precision → Don't send irrelevant information to the model.

---

## Technology Stack

### Backend

* Python
* FastAPI

### Database

* PostgreSQL

### Vector Database

* Qdrant

### AI Components

* Local Llama 3.2
* BAAI BGE Embeddings
* BM25 Retrieval
* Reciprocal Rank Fusion (RRF)
* CrossEncoder Reranker

### Messaging

* WhatsApp Cloud API

### Deployment

* Docker
* Docker Compose

---

## Project Structure

```text
app/
├── api/
├── core/
├── db/
├── models/
├── prompts/
├── providers/
├── rag/
├── repositories/
├── schemas/
├── services/
├── utils/
└── main.py

scripts/
├── test_bm25.py
├── test_hybrid.py
├── test_hybrid_rerank.py
├── test_rank_fusion.py
└── test_whatsapp.py

screenshots/
├── website-chatbot.png
└── whatsapp-chatbot.png
```

---

## Setup

### Clone Repository

git clone https://github.com/Baskar-forever/omnichannel-rag-chatbot.git

cd omnichannel-rag-chatbot

### Environment Variables

Create a .env file and configure:

DATABASE_URL=

QDRANT_HOST=
QDRANT_PORT=

WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_ID=

LLM_MODEL=

### Start Services

docker compose up -d

### Initialize Database

python init_db.py

### Run Application

uvicorn app.main:app --reload

---

## WhatsApp Configuration

1. Create a Meta Developer App
2. Configure WhatsApp Cloud API
3. Configure the Webhook URL
4. Set a Verify Token
5. Add Access Token and Phone Number ID to the .env file

Webhook Endpoint:

/api/whatsapp/webhook

---

## Deliverables

* Website AI Chatbot
* WhatsApp AI Chatbot
* Shared Knowledge Base
* Lead Collection System
* PostgreSQL Storage
* Source Attribution
* Docker Deployment
* Documentation

---

## Notes

* Shared knowledge base used by both Website and WhatsApp channels
* Lead information stored in PostgreSQL
* Message deduplication implemented for WhatsApp reliability
* Local Llama model used for response generation
* Retrieval pipeline optimized for both Recall and Precision
* Easily adaptable to different organizations by changing the knowledge source and prompts

---

Originally developed as a technical assessment project and later generalized into a reusable omnichannel RAG chatbot framework.
