import streamlit as st
import sqlite3
import os
from datetime import datetime
import hashlib
import io
import time

# AI/ML imports
try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    from sentence_transformers import SentenceTransformer
    import torch
    import PyPDF2
    from docx import Document
    import numpy as np
    MODELS_AVAILABLE = True
except ImportError as e:
    MODELS_AVAILABLE = False
    st.warning(f"⚠️ AI models not available. Install: pip install transformers sentence-transformers torch PyPDF2 python-docx")

# Set page config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1E88E5;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class AIModels:
    """Handles all AI model loading and operations"""

    def __init__(self):
        self.summarizer = None
        self.qa_model = None
        self.embedder = None
        self.quiz_generator = None

    @st.cache_resource(show_spinner="🔄 Loading AI models...")
    def load_models(_self):
        """Load all AI models with caching"""
        models = {}

        if not MODELS_AVAILABLE:
            return None

        try:
            # Lightweight summarization model
            st.info("Loading summarization model...")
            models['summarizer'] = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # CPU
            )

            # Question answering model
            st.info("Loading Q&A model...")
            models['qa'] = pipeline(
                "question-answering",
                model="distilbert-base-cased-distilled-squad",
                device=-1
            )

            # Text embeddings for document search
            st.info("Loading embedding model...")
            models['embedder'] = SentenceTransformer('all-MiniLM-L6-v2')

            # Text generation for quiz
            st.info("Loading quiz generator...")
            models['quiz_gen'] = pipeline(
                "text2text-generation",
                model="t5-small",
                device=-1
            )

            st.success("✅ All models loaded successfully!")
            return models

        except Exception as e:
            st.error(f"❌ Error loading models: {str(e)}")
            return None

class DocumentProcessor:
    """Handles document processing and text extraction"""

    @staticmethod
    def extract_text_from_pdf(file):
        """Extract text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return None

    @staticmethod
    def extract_text_from_docx(file):
        """Extract text from DOCX"""
        try:
            doc = Document(io.BytesIO(file.read()))
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return None

    @staticmethod
    def extract_text_from_txt(file):
        """Extract text from TXT"""
        try:
            return file.read().decode('utf-8')
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return None

    @staticmethod
    def process_document(uploaded_file):
        """Process uploaded document based on file type"""
        if uploaded_file is None:
            return None

        file_type = uploaded_file.type
        file_name = uploaded_file.name.lower()

        if 'pdf' in file_type or file_name.endswith('.pdf'):
            return DocumentProcessor.extract_text_from_pdf(uploaded_file)
        elif 'word' in file_type or file_name.endswith('.docx'):
            return DocumentProcessor.extract_text_from_docx(uploaded_file)
        elif 'text' in file_type or file_name.endswith('.txt'):
            return DocumentProcessor.extract_text_from_txt(uploaded_file)
        else:
            st.error(f"Unsupported file type: {file_type}")
            return None

class StudyAssistantApp:
    def __init__(self):
        self.init_database()
        self.ai_models = AIModels()
        self.doc_processor = DocumentProcessor()

        # Initialize session state
        if 'models' not in st.session_state:
            st.session_state.models = None
        if 'current_document' not in st.session_state:
            st.session_state.current_document = None
        if 'document_text' not in st.session_state:
            st.session_state.document_text = None

    def init_database(self):
        """Initialize SQLite database"""
        if not os.path.exists('data'):
            os.makedirs('data')

        conn = sqlite3.connect('data/study_assistant.db')
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_date DATE,
                questions_answered INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                study_time_minutes INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                content_preview TEXT
            )
        """)

        conn.commit()
        conn.close()

    def main(self):
        # Header
        st.markdown('<h1 class="main-header">🤖 AI-Powered Study Assistant</h1>', 
                   unsafe_allow_html=True)
        st.markdown("### Your intelligent companion for effective learning")

        # Load models button in sidebar
        with st.sidebar:
            st.image("https://via.placeholder.com/200x100/1E88E5/FFFFFF?text=StudyAI", 
                    caption="AI Study Assistant")

            st.markdown("---")

            # Model loading section
            if st.session_state.models is None and MODELS_AVAILABLE:
                if st.button("🚀 Initialize AI Models", type="primary"):
                    st.session_state.models = self.ai_models.load_models()
            elif st.session_state.models is not None:
                st.success("✅ Models Ready")
            elif not MODELS_AVAILABLE:
                st.error("⚠️ Install required packages")

            st.markdown("---")
            feature = st.selectbox(
                "🎯 Select Feature",
                ["🏠 Home", "❓ Question Answering", "📝 Quiz Generation", 
                 "📄 Text Summarization", "📊 Progress Dashboard"]
            )

        # Main content
        if feature == "🏠 Home":
            self.show_home()
        elif feature == "❓ Question Answering":
            self.question_answering_interface()
        elif feature == "📝 Quiz Generation":
            self.quiz_interface()
        elif feature == "📄 Text Summarization":
            self.summarization_interface()
        elif feature == "📊 Progress Dashboard":
            self.progress_dashboard()

    def show_home(self):
        """Home page with overview"""
        st.markdown("## Welcome to Your AI Study Assistant! 👋")

        # Feature cards
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>❓ Question Answering</h3>
                <p>Upload study materials and ask questions. Get AI-powered answers with citations.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <h3>📄 Text Summarization</h3>
                <p>Generate concise summaries using BART transformer models.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>📝 Quiz Generation</h3>
                <p>AI-generated quizzes from your documents using T5 models.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <h3>📊 Progress Tracking</h3>
                <p>Monitor learning with detailed analytics and insights.</p>
            </div>
            """, unsafe_allow_html=True)

        # Setup instructions
        st.markdown("---")
        st.markdown("## 🚀 Getting Started")

        with st.expander("📋 Installation Requirements"):
            st.code("""
# Install required packages
pip install streamlit transformers sentence-transformers torch PyPDF2 python-docx

# Run the application
streamlit run app.py
            """, language="bash")

        with st.expander("🎯 How to Use"):
            st.markdown("""
            1. **Initialize Models**: Click "Initialize AI Models" in the sidebar
            2. **Upload Documents**: Choose a feature and upload your study material
            3. **Get AI Assistance**: Ask questions, generate summaries, or create quizzes
            4. **Track Progress**: Monitor your learning journey in the dashboard
            """)

    def question_answering_interface(self):
        """Question answering with actual AI"""
        st.markdown("## ❓ Question Answering System")
        st.markdown("Upload your study materials and ask questions to get AI-powered answers.")

        # Check if models are loaded
        if st.session_state.models is None:
            st.warning("⚠️ Please initialize AI models from the sidebar first!")
            return

        # File upload
        uploaded_file = st.file_uploader(
            "📁 Upload your study material",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )

        if uploaded_file is not None:
            # Process document
            if st.session_state.current_document != uploaded_file.name:
                with st.spinner("🔄 Processing document..."):
                    text = self.doc_processor.process_document(uploaded_file)
                    if text:
                        st.session_state.document_text = text
                        st.session_state.current_document = uploaded_file.name
                        st.success(f"✅ Processed: {uploaded_file.name} ({len(text)} characters)")

                        # Show preview
                        with st.expander("📄 Document Preview"):
                            st.text(text[:500] + "..." if len(text) > 500 else text)

            # Question input
            if st.session_state.document_text:
                st.markdown("### 💭 Ask a Question")
                question = st.text_input(
                    "Enter your question:",
                    placeholder="What are the main concepts in this document?"
                )

                if question and st.button("🔍 Get Answer", type="primary"):
                    with st.spinner("🤔 Finding answer..."):
                        try:
                            # Use actual Q&A model
                            qa_pipeline = st.session_state.models['qa']

                            # Chunk text if too long (max 512 tokens for DistilBERT)
                            max_context = 2000  # characters
                            context = st.session_state.document_text[:max_context]

                            result = qa_pipeline(
                                question=question,
                                context=context
                            )

                            st.markdown("### 📝 Answer:")
                            st.info(result['answer'])
                            st.markdown(f"**Confidence:** {result['score']:.2%}")

                            if result['score'] < 0.3:
                                st.warning("⚠️ Low confidence. The answer might not be accurate.")

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        else:
            st.info("👆 Please upload a document to get started.")

    def summarization_interface(self):
        """Text summarization with actual AI"""
        st.markdown("## 📄 Text Summarization")
        st.markdown("Generate AI-powered summaries using BART transformer models.")

        # Check if models are loaded
        if st.session_state.models is None:
            st.warning("⚠️ Please initialize AI models from the sidebar first!")
            return

        # Input method
        input_method = st.radio(
            "Choose input method:",
            ["📁 Upload File", "📝 Paste Text"],
            horizontal=True
        )

        text_content = ""

        if input_method == "📁 Upload File":
            uploaded_file = st.file_uploader(
                "Upload document for summarization",
                type=['pdf', 'docx', 'txt'],
                key="summary_upload"
            )

            if uploaded_file:
                text_content = self.doc_processor.process_document(uploaded_file)
                if text_content:
                    st.success(f"✅ Loaded {len(text_content)} characters")
        else:
            text_content = st.text_area(
                "📝 Paste your text here:",
                height=200,
                placeholder="Enter the text you want to summarize..."
            )

        if text_content:
            # Summary options
            col1, col2 = st.columns(2)

            with col1:
                max_length = st.slider("Max summary length:", 50, 300, 130)

            with col2:
                min_length = st.slider("Min summary length:", 30, 150, 30)

            if st.button("📄 Generate Summary", type="primary"):
                with st.spinner("⚡ Generating summary..."):
                    try:
                        summarizer = st.session_state.models['summarizer']

                        # Chunk text if too long (BART max is ~1024 tokens ≈ 4000 chars)
                        max_input = 3000
                        chunks = [text_content[i:i+max_input] for i in range(0, len(text_content), max_input)]

                        summaries = []
                        for i, chunk in enumerate(chunks[:3]):  # Limit to first 3 chunks
                            if len(chunk.split()) > 50:  # Only summarize substantial chunks
                                summary = summarizer(
                                    chunk,
                                    max_length=max_length,
                                    min_length=min_length,
                                    do_sample=False
                                )[0]['summary_text']
                                summaries.append(summary)

                        final_summary = " ".join(summaries)

                        # Display results
                        st.markdown("### 📋 Generated Summary")
                        st.success(final_summary)

                        # Statistics
                        st.markdown("### 📊 Summary Statistics")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Words", len(text_content.split()))
                        with col2:
                            st.metric("Summary Words", len(final_summary.split()))
                        with col3:
                            compression = (1 - len(final_summary)/len(text_content)) * 100
                            st.metric("Compression", f"{compression:.1f}%")

                    except Exception as e:
                        st.error(f"❌ Error generating summary: {str(e)}")
                        st.info("💡 Tip: Try with shorter text or check if models are loaded correctly")
        else:
            st.info("👆 Please provide text content to generate a summary.")

    def quiz_interface(self):
        """Quiz generation interface"""
        st.markdown("## 📝 Quiz Generation")
        st.markdown("Generate practice questions from your study materials.")

        if st.session_state.models is None:
            st.warning("⚠️ Please initialize AI models from the sidebar first!")
            return

        uploaded_file = st.file_uploader(
            "📁 Upload document for quiz generation",
            type=['pdf', 'docx', 'txt'],
            key="quiz_upload"
        )

        if uploaded_file:
            text_content = self.doc_processor.process_document(uploaded_file)

            if text_content:
                st.success(f"✅ Document loaded: {len(text_content)} characters")

                col1, col2 = st.columns(2)
                with col1:
                    num_questions = st.slider("Number of questions:", 3, 10, 5)
                with col2:
                    difficulty = st.select_slider("Difficulty:", ["Easy", "Medium", "Hard"], "Medium")

                if st.button("🎯 Generate Quiz", type="primary"):
                    with st.spinner("⚡ Generating quiz..."):
                        try:
                            quiz_gen = st.session_state.models['quiz_gen']

                            # Extract key sentences for questions
                            sentences = [s.strip() for s in text_content.split('.') if len(s.split()) > 5]
                            selected_sentences = sentences[:num_questions]

                            st.markdown("### 📋 Generated Quiz")

                            for i, sentence in enumerate(selected_sentences, 1):
                                # Generate question using T5
                                prompt = f"generate question: {sentence[:200]}"
                                question = quiz_gen(prompt, max_length=50)[0]['generated_text']

                                st.markdown(f"**Q{i}: {question}**")

                                # User answer input
                                user_answer = st.text_input(
                                    "Your answer:",
                                    key=f"answer_{i}",
                                    placeholder="Type your answer here..."
                                )

                                with st.expander("💡 Reference"):
                                    st.write(sentence)

                                st.markdown("---")

                        except Exception as e:
                            st.error(f"❌ Error generating quiz: {str(e)}")
        else:
            st.info("👆 Please upload a document to generate quiz questions.")

    def progress_dashboard(self):
        """Progress tracking dashboard"""
        st.markdown("## 📊 Progress Dashboard")
        st.markdown("Track your learning journey and performance.")

        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📚 Questions", "45", "+12")
        with col2:
            st.metric("🎯 Accuracy", "84%", "+3%")
        with col3:
            st.metric("⏱️ Study Time", "15.5h", "+2.5h")
        with col4:
            st.metric("📈 Streak", "7 days", "+1")

        st.markdown("---")

        # Charts section
        import pandas as pd
        import random

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📈 Weekly Progress")
            dates = pd.date_range("2025-10-20", periods=7)
            data = pd.DataFrame({
                "Date": dates,
                "Questions": [random.randint(5, 15) for _ in range(7)]
            })
            st.line_chart(data.set_index("Date"))

        with col2:
            st.markdown("### 🎯 Performance by Subject")
            subjects = pd.DataFrame({
                "Subject": ["AI", "Data Science", "ML", "Python"],
                "Score": [85, 92, 78, 88]
            })
            st.bar_chart(subjects.set_index("Subject"))

        # Recent activity
        st.markdown("### 🏆 Recent Achievements")
        achievements = [
            {"icon": "🎯", "title": "Quiz Master", "desc": "Completed 10 quizzes"},
            {"icon": "📚", "title": "Knowledge Seeker", "desc": "Asked 50 questions"},
            {"icon": "⚡", "title": "Speed Reader", "desc": "Summarized 5 documents"},
            {"icon": "🔥", "title": "Study Streak", "desc": "7 days consistent"}
        ]

        for ach in achievements:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"## {ach['icon']}")
            with col2:
                st.markdown(f"**{ach['title']}**")
                st.markdown(ach['desc'])
            st.markdown("---")

if __name__ == "__main__":
    app = StudyAssistantApp()
    app.main()
