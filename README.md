
![LatentScience Logo](public/default-monochrome.svg)

# LatentScience

A web application that finds semantic connections between research papers using embeddings and AI-powered explanations.

## Main idea

Similar scientific concepts often look different across academic domains without researchers realising they are speaking the same language. We developed LatentScience to leverage AI to identify connections between papers that may not be explicit or obvious.

We have included some hand-picked examples in the [database.csv](https://github.com/CompMotifs/LatentScience/blob/main/database.csv) file, which contains 17 example pairs of papers from source and target domains that share ideas. Paper contributions are increasingly decomposed into abstract components to highlight conceptual links.

We hope that our approach can inspire cross-disciplinary ideation, empower researchers, and accelerate scientific discovery.


## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Modal account ([sign up at modal.com](https://modal.com))
- OpenAI API key
- PostgreSQL database (optional for local development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd paper-links-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Modal CLI**
   ```bash
   pip install modal
   modal token new
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database URL
   ```

5. **Create Modal secrets**
   ```bash
   # OpenAI API key
   modal secret create openai-secret OPENAI_API_KEY=your_openai_key_here
   
   # Database connection (if using PostgreSQL)
   modal secret create database-secrets DATABASE_URL=postgresql://user:pass@host:port/dbname
   ```

## 🏃‍♂️ Running the Application

### Option 1: Full Modal Deployment (Recommended)

1. **Deploy to Modal**
   ```bash
   modal deploy app/main.py
   ```

2. **Access the web interface**
   - The deployment will provide URLs for:
     - Web interface: `https://your-app-name--web-app.modal.run`
     - API endpoint: `https://your-app-name--api-endpoint.modal.run`

### Option 2: Local Development with Modal Services

1. **Run Modal services locally**
   ```bash
   modal serve app/main.py
   ```

2. **Access the application**
   - Web interface: `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`

### Option 3: Pure Local Development (Limited)

1. **Set up local database**
   ```bash
   # Install and start PostgreSQL locally
   createdb paper_links
   ```

2. **Run the FastAPI server**
   ```bash
   cd web
   uvicorn api:app --reload --port 8000
   ```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Database
DATABASE_URL=postgresql://user:password@localhost:5432/paper_links
# Or for SQLite (local development)
DATABASE_URL=sqlite:///./papers.db

# Optional - Model Configuration
DEFAULT_EMBEDDING_MODEL=text-embedding-ada-002
SIMILARITY_THRESHOLD=0.7
MAX_RESULTS=10
```

### Modal Configuration (modal.toml)

```toml
[build]
python_version = "3.9"

[secrets]
openai-secret = ["OPENAI_API_KEY"]
database-secrets = ["DATABASE_URL"]

[volumes]
paper-links-db = "/data"
model-cache = "/cache"
```

## 📚 API Usage

### Search for Similar Papers

```bash
curl -X POST "https://your-app--api-endpoint.modal.run/api/search-papers" \
  -H "Content-Type: application/json" \
  -d '{
    "paper": {
      "title": "Attention Is All You Need",
      "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
      "authors": ["Ashish Vaswani", "Noam Shazeer"]
    },
    "research_question": {
      "question": "What are the latest developments in transformer architectures?"
    },
    "max_results": 10,
    "similarity_threshold": 0.7
  }'
```

### Generate Embedding

```bash
curl -X POST "https://your-app--api-endpoint.modal.run/api/generate-embedding" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your paper text here...",
    "model": "text-embedding-ada-002"
  }'
```

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run specific test file
pytest tests/test_embedding_service.py

# Run with coverage
pytest --cov=app tests/
```

### Manual Testing

1. **Test embedding generation**
   ```bash
   modal run services.embedding_service::test_embedding
   ```

2. **Test similarity calculation**
   ```bash
   modal run services.similarity_service::test_similarity
   ```

## 🛠️ Development

### Project Structure

```
paper-links-app/
├── app/              # Core application and models
├── services/         # Business logic services
├── web/              # Web interface and API
├── database/         # Database models and migrations
├── prompts/          # LLM prompts and templates
└── utils/            # Utility functions
```

### Adding New Features

1. **Create a new service**
   ```python
   # services/new_service.py
   from app.models.your_model import YourModel
   
   class NewService:
       def process(self, data):
           # Your logic here
           pass
   ```

2. **Add to Modal app**
   ```python
   # app/main.py
   @app.cls(image=image)
   class NewServiceModal:
       def __init__(self):
           self.service = NewService()
       
       @modal.method()
       def process(self, data):
           return self.service.process(data)
   ```

3. **Add API endpoint**
   ```python
   # web/api.py
   @api.post("/api/new-endpoint")
   async def new_endpoint(request: YourModel):
       # Call Modal service
       return result
   ```

## 🚨 Toy Prototype Considerations

### What's Currently Implemented (Skeleton)
- ✅ Basic project structure
- ✅ Pydantic models for data validation
- ✅ Modal app configuration
- ✅ Service interfaces
- ✅ Basic API endpoints

### What You Need to Complete for MVP
- [ ] Complete HTML/CSS/JS for the web interface
- [ ] Implement actual embedding generation (currently mocked)
- [ ] Set up real database connection and operations
- [ ] Complete similarity calculation logic
- [ ] Implement explanation generation
- [ ] Add error handling and logging

### Known Limitations (Toy Prototype)
- 🔴 **No real paper data**: You'll need to add actual papers to test
- 🔴 **Simplified similarity search**: Not optimized for large datasets
- 🔴 **No authentication**: Anyone can access the service
- 🔴 **No rate limiting**: Could be expensive with OpenAI API
- 🔴 **No caching**: Every request hits the LLM APIs
- 🔴 **Basic error handling**: Needs improvement for production

### Cost Considerations
- **OpenAI API costs**: ~$0.0001 per 1K tokens for embeddings
- **Modal compute**: Pay-per-use, typically $0.000X per second
- **Database storage**: Minimal for prototype, scales with paper count

### Performance Expectations
- **Embedding generation**: 1-2 seconds per paper
- **Similarity search**: Milliseconds for small datasets
- **Explanation generation**: 2-5 seconds per explanation
- **Cold start**: 5-10 seconds for Modal functions

## 🔍 Troubleshooting

### Common Issues

**Modal deployment fails**
```bash
# Check your token
modal token new

# Verify secrets are set
modal secret list
```

**OpenAI API errors**
```bash
# Check your API key
export OPENAI_API_KEY=your_key_here
python -c "import openai; print(openai.Model.list())"
```

**Database connection issues**
```bash
# For local PostgreSQL
pg_isready -h localhost -p 5432

# Check SQLAlchemy connection
python -c "from app.main import DatabaseService; db = DatabaseService(); print('Connected!')"
```

### Debugging

1. **Check Modal logs**
   ```bash
   modal logs your-app-name
   ```

2. **Enable debug mode**
   ```bash
   export DEBUG=true
   modal serve app/main.py
   ```

3. **Test individual services**
   ```bash
   modal run services.embedding_service::EmbeddingService.generate_embedding --text="test"
   ```

## 📈 Next Steps (Beyond Prototype)

### Performance Optimization
- [ ] Implement vector database (Pinecone/Weaviate)
- [ ] Add Redis caching layer
- [ ] Optimize embedding batch processing
- [ ] Implement async processing queues

### Production Features
- [ ] User authentication and rate limiting
- [ ] Paper upload and parsing (PDF support)
- [ ] Advanced search filters
- [ ] Export and sharing features
- [ ] Admin dashboard for monitoring

### Data Sources
- [ ] arXiv API integration
- [ ] PubMed/MEDLINE connector
- [ ] Google Scholar scraping
- [ ] Manual paper upload system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- Check the [troubleshooting section](#-troubleshooting)
- Review Modal documentation: [docs.modal.com](https://docs.modal.com)
- Open an issue for bugs or feature requests
