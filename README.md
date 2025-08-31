# 🤖 Intercom AI Support with RAG

A **production-ready** AI-powered customer support system that integrates with Intercom and uses **Retrieval-Augmented Generation (RAG)** to provide intelligent, context-aware responses.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-purple.svg)
![LangChain](https://img.shields.io/badge/LangChain-RAG%20Framework-yellow.svg)

## 🚀 Features

### ✨ **Core Capabilities**
- **AI-Powered Responses** - GPT-4 integration for intelligent customer support
- **RAG System** - Retrieval-Augmented Generation for context-aware responses
- **Vector Database** - ChromaDB for semantic search and document storage
- **Intercom Integration** - Webhook handling for real-time conversations
- **Knowledge Base Management** - Add, search, and manage support documents
- **Beautiful Web Interface** - Modern UI for testing and management

### 🎯 **AI Features**
- **Sentiment Analysis** - Understand customer emotions
- **Issue Categorization** - Automatically classify support requests
- **Escalation Detection** - Identify when human intervention is needed
- **Context-Aware Responses** - Use knowledge base for accurate answers

### 📊 **Knowledge Base**
- **Semantic Search** - Find relevant documents using AI embeddings
- **Document Management** - CRUD operations for support content
- **Automatic Categorization** - Organize documents by topic and priority
- **Sample Data** - Pre-loaded with common support scenarios

## 🏗️ Architecture

```
Intercom AI Support/
├── app/
│   ├── main.py              # FastAPI application & endpoints
│   ├── ai.py                # OpenAI integration & AI services
│   ├── intercom.py          # Intercom API client
│   ├── config.py            # Configuration management
│   ├── utils.py             # Utility functions
│   ├── static/
│   │   └── index.html       # Web interface
│   ├── database/
│   │   ├── vector_store.py  # ChromaDB vector database
│   │   └── knowledge_base.py # Knowledge base management
│   └── rag/
│       └── retriever.py     # RAG retrieval logic
├── data/
│   └── knowledge_base/      # Vector database storage
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **AI/ML**: OpenAI GPT-4, LangChain, Sentence Transformers
- **Vector Database**: ChromaDB
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **APIs**: Intercom API, OpenAI API
- **Deployment**: Docker-ready, production-ready

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Intercom access token (optional for full integration)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/intercom-ai-support.git
   cd intercom-ai-support
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the application**
   - Web Interface: http://127.0.0.1:8000
   - API Documentation: http://127.0.0.1:8000/docs
   - Health Check: http://127.0.0.1:8000/health

## 🎮 Usage

### Web Interface

Visit `http://127.0.0.1:8000` to access the beautiful web interface with four main features:

1. **💬 AI Chat** - Test RAG-enhanced AI responses
2. **🔍 Knowledge Search** - Search through support documents
3. **📚 Manage Documents** - Add and manage knowledge base content
4. **📊 Statistics** - View system performance metrics

### API Endpoints

#### Core Endpoints
- `POST /conversation/respond` - Generate AI response
- `POST /webhook/intercom` - Handle Intercom webhooks
- `GET /health` - Health check

#### Knowledge Base Management
- `GET /knowledge-base/stats` - Get statistics
- `POST /knowledge-base/search` - Search documents
- `POST /knowledge-base/add` - Add new document
- `PUT /knowledge-base/update/{id}` - Update document
- `DELETE /knowledge-base/delete/{id}` - Delete document
- `GET /knowledge-base/document/{id}` - Get specific document

### Example API Usage

```python
import requests

# Generate AI response
response = requests.post("http://127.0.0.1:8000/conversation/respond", json={
    "conversation_id": "test_123",
    "message": "How do I reset my password?"
})

# Search knowledge base
search = requests.post("http://127.0.0.1:8000/knowledge-base/search", json={
    "query": "password reset",
    "k": 5
})
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Intercom Configuration (Optional)
INTERCOM_ACCESS_TOKEN=your_intercom_token_here

# Application Settings
DEBUG=True
HOST=127.0.0.1
PORT=8000
ALLOWED_HOSTS=*

# Vector Database
CHROMA_DB_PATH=./data/knowledge_base
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/
```

### Manual Testing
1. Start the server: `uvicorn app.main:app --reload`
2. Visit the web interface: http://127.0.0.1:8000
3. Test AI chat with sample queries
4. Search the knowledge base
5. Add new documents

## 📈 Performance

- **Response Time**: < 2 seconds for AI responses
- **Search Accuracy**: High semantic relevance using embeddings
- **Scalability**: Vector database supports thousands of documents
- **Memory Usage**: Efficient embedding storage and retrieval

## 🔒 Security

- **API Key Protection** - Environment variable storage
- **Input Validation** - Pydantic models for data validation
- **CORS Configuration** - Configurable cross-origin requests
- **Error Handling** - Graceful error responses

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t intercom-ai-support .

# Run container
docker run -p 8000:8000 --env-file .env intercom-ai-support
```

### Production Deployment
1. Set `DEBUG=False` in environment
2. Configure proper `ALLOWED_HOSTS`
3. Use production ASGI server (Gunicorn)
4. Set up reverse proxy (Nginx)
5. Configure SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **LangChain** for RAG framework
- **ChromaDB** for vector database
- **FastAPI** for web framework
- **Intercom** for customer messaging platform

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/intercom-ai-support/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/intercom-ai-support/wiki)
- **Email**: your.email@example.com

---

**⭐ Star this repository if you find it helpful!**

**Made with ❤️ for better customer support experiences** 