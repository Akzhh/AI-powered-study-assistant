# 🤖 AI-Powered Study Assistant

A comprehensive AI-powered study assistant that helps students learn more effectively through intelligent question answering, quiz generation, text summarization, and progress tracking.

## ✨ Features

- **📝 Question Answering**: Upload study materials and get instant answers to your questions using advanced RAG (Retrieval-Augmented Generation) technology
- **🎯 Quiz Generation**: Automatically generate custom quizzes from your documents with multiple difficulty levels
- **📄 Text Summarization**: Create concise summaries of lengthy documents and extract key points
- **📊 Progress Tracking**: Monitor your learning progress with detailed analytics and performance insights

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project files**
2. **Create a virtual environment**
   ```bash
   python -m venv study_assistant_env
   source study_assistant_env/bin/activate  # On Windows: study_assistant_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 🛠️ Technology Stack

- **Backend**: Python, Streamlit
- **AI Models**: Hugging Face Transformers, Sentence Transformers
- **Database**: SQLite
- **Vector Search**: FAISS
- **Document Processing**: PyPDF2, python-docx
- **Visualization**: Plotly

## 📁 Project Structure

```
ai-study-assistant/
├── app.py                    # Main Streamlit application
├── complete-dev-guide.md     # Comprehensive development guide  
├── study_assistant_schema.sql # Database schema
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── data/                    # Data storage (created automatically)
    └── study_assistant.db   # SQLite database
```

## 🎯 Usage Guide

### 1. Question Answering
1. Navigate to the "Question Answering" section
2. Upload your study material (PDF, DOCX, or TXT)
3. Wait for the document to be processed
4. Ask questions about the content
5. Receive instant answers with source citations

### 2. Quiz Generation  
1. Go to the "Quiz Generation" section
2. Upload a document
3. Configure quiz parameters (number of questions, difficulty)
4. Generate and take the quiz
5. Check answers and explanations

### 3. Text Summarization
1. Access the "Text Summarization" feature
2. Upload a document or paste text
3. Choose summary length and type
4. Generate summary and key points

### 4. Progress Dashboard
1. View the "Progress Dashboard" 
2. Monitor your learning metrics
3. Track study streaks and achievements
4. Analyze performance trends

## 🔧 Advanced Configuration

### Environment Variables
Create a `.env` file for API keys (optional):
```
OPENAI_API_KEY=your_openai_key_here
HUGGINGFACE_API_TOKEN=your_hf_token_here
```

### Model Configuration
The app uses these AI models by default:
- **Question Answering**: `distilbert-base-cased-distilled-squad`
- **Embeddings**: `all-MiniLM-L6-v2`
- **Summarization**: `facebook/bart-large-cnn`

## 📊 Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| Document Upload | PDF, DOCX, TXT support | ✅ |
| Question Answering | RAG-based Q&A system | ✅ |
| Quiz Generation | AI-generated quizzes | ✅ |
| Text Summarization | Extractive & Abstractive | ✅ |
| Progress Tracking | Learning analytics | ✅ |
| User Authentication | Login/Signup system | 🔄 |
| Multi-language Support | Non-English documents | 🔄 |

## 🚧 Development

### Running Tests
```bash
python -m pytest tests/ -v
```

### Code Formatting
```bash
black app.py
flake8 app.py
```

### Adding New Features
1. Follow the architecture in `complete-dev-guide.md`
2. Add new modules in separate files
3. Import and integrate in `app.py`
4. Update database schema if needed
5. Add tests for new functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable  
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

- Check the comprehensive development guide: `complete-dev-guide.md`
- Review the database schema: `study_assistant_schema.sql`
- Open an issue for bugs or feature requests

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Cloud Deployment
- **Streamlit Cloud**: Connect your GitHub repo
- **Heroku**: Use the Docker configuration
- **AWS/GCP**: Deploy with container services

## 🎓 Educational Value

This project demonstrates:
- Modern AI integration in educational applications
- RAG (Retrieval-Augmented Generation) implementation
- Full-stack development with Python
- Database design and management
- User interface design with Streamlit
- AI model integration and optimization

Perfect for 2nd-year AI/Data Science students to learn practical AI application development!

## 🔗 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Hugging Face Transformers](https://huggingface.co/transformers)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [LangChain Documentation](https://python.langchain.com)

---

**Built By Akash.B**
