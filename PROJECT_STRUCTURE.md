# 📁 Project Structure

This document provides a detailed overview of the Intercom AI Support project structure and the purpose of each component.

## 🏗️ Directory Structure

```
Intercom AI Support/
├── 📁 app/                          # Main application package
│   ├── 📁 __init__.py              # Package marker
│   ├── 📄 main.py                  # FastAPI application & endpoints
│   ├── 📄 ai.py                    # OpenAI integration & AI services
│   ├── 📄 intercom.py              # Intercom API client
│   ├── 📄 config.py                # Configuration management
│   ├── 📄 utils.py                 # Utility functions
│   ├── 📁 static/                  # Static files (web interface)
│   │   └── 📄 index.html           # Beautiful web UI
│   ├── 📁 database/                # Database layer
│   │   ├── 📄 __init__.py          # Package marker
│   │   ├── 📄 vector_store.py      # ChromaDB vector database
│   │   └── 📄 knowledge_base.py    # Knowledge base management
│   └── 📁 rag/                     # RAG (Retrieval-Augmented Generation)
│       ├── 📄 __init__.py          # Package marker
│       └── 📄 retriever.py         # RAG retrieval logic
├── 📁 data/                        # Data storage
│   └── 📁 knowledge_base/          # Vector database files
├── 📁 tests/                       # Test suite
│   └── 📄 test_basic.py            # Basic unit tests
├── 📁 .github/                     # GitHub configuration
│   └── 📁 workflows/               # GitHub Actions
│       └── 📄 ci.yml               # CI/CD pipeline
├── 📄 .env                         # Environment variables (gitignored)
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 requirements.txt             # Python dependencies
├── 📄 Dockerfile                   # Docker configuration
├── 📄 docker-compose.yml           # Docker Compose setup
├── 📄 LICENSE                      # MIT License
├── 📄 README.md                    # Main documentation
└── 📄 PROJECT_STRUCTURE.md         # This file
```

## 🔧 Core Components

### **📄 app/main.py**
- **Purpose**: FastAPI application entry point
- **Key Features**:
  - API endpoints for conversation handling
  - Knowledge base management endpoints
  - Webhook processing for Intercom
  - Static file serving for web interface
  - CORS configuration
  - Health check endpoint

### **📄 app/ai.py**
- **Purpose**: OpenAI integration and AI services
- **Key Features**:
  - GPT-4 response generation
  - Sentiment analysis
  - Issue categorization
  - Escalation detection
  - RAG context integration
  - Conversation management

### **📄 app/intercom.py**
- **Purpose**: Intercom API client
- **Key Features**:
  - Webhook signature validation
  - Conversation retrieval
  - Message sending
  - User management
  - API rate limiting

### **📄 app/config.py**
- **Purpose**: Configuration management
- **Key Features**:
  - Environment variable handling
  - Settings validation
  - Default configurations
  - API key management

### **📄 app/utils.py**
- **Purpose**: Utility functions
- **Key Features**:
  - Message sanitization
  - Logging utilities
  - Data validation helpers
  - Common helper functions

## 🗄️ Database Layer

### **📄 app/database/vector_store.py**
- **Purpose**: ChromaDB vector database management
- **Key Features**:
  - Document embedding and storage
  - Semantic search functionality
  - Collection management
  - Metadata handling
  - Performance optimization

### **📄 app/database/knowledge_base.py**
- **Purpose**: Knowledge base document management
- **Key Features**:
  - CRUD operations for documents
  - Sample data initialization
  - Document categorization
  - Export/import functionality
  - Statistics and analytics

## 🤖 RAG System

### **📄 app/rag/retriever.py**
- **Purpose**: Retrieval-Augmented Generation logic
- **Key Features**:
  - Context retrieval from knowledge base
  - Query enhancement
  - Relevance scoring
  - Context building for AI responses
  - Smart filtering and ranking

## 🌐 Web Interface

### **📄 app/static/index.html**
- **Purpose**: Beautiful web interface
- **Key Features**:
  - Modern, responsive design
  - Four main tabs:
    - AI Chat testing
    - Knowledge base search
    - Document management
    - System statistics
  - Real-time API integration
  - Loading states and error handling

## 🐳 Deployment

### **📄 Dockerfile**
- **Purpose**: Container configuration
- **Key Features**:
  - Multi-stage build optimization
  - Security hardening
  - Health checks
  - Non-root user execution
  - Production-ready configuration

### **📄 docker-compose.yml**
- **Purpose**: Multi-service deployment
- **Key Features**:
  - Service orchestration
  - Volume management
  - Environment configuration
  - Health monitoring
  - Easy development setup

## 🧪 Testing

### **📄 tests/test_basic.py**
- **Purpose**: Basic unit tests
- **Key Features**:
  - API endpoint testing
  - AI service testing
  - Knowledge base operations
  - Error handling validation

## 🔄 CI/CD Pipeline

### **📄 .github/workflows/ci.yml**
- **Purpose**: Automated testing and deployment
- **Key Features**:
  - Multi-Python version testing
  - Code quality checks (linting)
  - Security scanning
  - Docker image testing
  - Coverage reporting

## 📋 Configuration Files

### **📄 requirements.txt**
- **Purpose**: Python dependencies
- **Key Dependencies**:
  - FastAPI for web framework
  - OpenAI for AI integration
  - ChromaDB for vector database
  - LangChain for RAG framework
  - Pydantic for data validation

### **📄 .env.example**
- **Purpose**: Environment variable template
- **Key Variables**:
  - OpenAI API key
  - Intercom credentials
  - Application settings
  - Database configuration

### **📄 .gitignore**
- **Purpose**: Git ignore rules
- **Excluded Items**:
  - Environment files
  - Python cache files
  - Virtual environments
  - Database files
  - IDE configurations

## 🚀 Quick Start Guide

1. **Clone the repository**
2. **Copy `.env.example` to `.env` and configure**
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Start the server**: `uvicorn app.main:app --reload`
5. **Access the web interface**: http://127.0.0.1:8000

## 🔍 Key Features by Component

| Component | Primary Function | Key Capabilities |
|-----------|-----------------|------------------|
| **main.py** | API Gateway | Endpoint routing, webhook handling |
| **ai.py** | AI Engine | GPT-4 integration, RAG enhancement |
| **intercom.py** | External API | Intercom integration, webhook validation |
| **vector_store.py** | Data Storage | Vector embeddings, semantic search |
| **knowledge_base.py** | Content Management | Document CRUD, categorization |
| **retriever.py** | RAG Logic | Context retrieval, query enhancement |
| **index.html** | User Interface | Web UI, real-time testing |

## 📊 Architecture Flow

```
User Request → FastAPI (main.py) → AI Service (ai.py) → RAG (retriever.py) → 
Knowledge Base (knowledge_base.py) → Vector Store (vector_store.py) → 
Response Generation → User Interface (index.html)
```

This modular architecture ensures:
- **Scalability**: Each component can be scaled independently
- **Maintainability**: Clear separation of concerns
- **Testability**: Isolated components for easy testing
- **Extensibility**: Easy to add new features or integrations 