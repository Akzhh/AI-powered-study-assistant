import streamlit as st
import sqlite3
import os
from datetime import datetime
import hashlib

# Set page config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
</style>
""", unsafe_allow_html=True)

class StudyAssistantApp:
    def __init__(self):
        self.init_database()

    def init_database(self):
        """Initialize SQLite database"""
        if not os.path.exists('data'):
            os.makedirs('data')

        conn = sqlite3.connect('data/study_assistant.db')
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create study sessions table
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

        conn.commit()
        conn.close()

    def main(self):
        # Header
        st.markdown('<h1 class="main-header">🤖 AI-Powered Study Assistant</h1>', 
                   unsafe_allow_html=True)
        st.markdown("### Your intelligent companion for effective learning")

        # Sidebar navigation
        with st.sidebar:
            st.image("https://via.placeholder.com/200x100/1E88E5/FFFFFF?text=StudyAI", 
                    caption="AI Study Assistant")

            st.markdown("---")
            feature = st.selectbox(
                "🎯 Select Feature",
                ["🏠 Home", "❓ Question Answering", "📝 Quiz Generation", 
                 "📄 Text Summarization", "📊 Progress Dashboard"]
            )

            st.markdown("---")
            st.markdown("### 🚀 Quick Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📚 Documents", "12")
            with col2:
                st.metric("🎯 Accuracy", "85%")

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
        st.markdown("## Welcome to Your AI Study Assistant! 👋")

        # Feature overview
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>❓ Question Answering</h3>
                <p>Upload your study materials and ask questions. Get instant, accurate answers with source citations.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <h3>📄 Text Summarization</h3>
                <p>Automatically generate concise summaries of long documents and extract key points.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>📝 Quiz Generation</h3>
                <p>Generate custom quizzes from your study materials with multiple difficulty levels.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <h3>📊 Progress Tracking</h3>
                <p>Monitor your learning progress with detailed analytics and performance insights.</p>
            </div>
            """, unsafe_allow_html=True)

        # Getting started section
        st.markdown("---")
        st.markdown("## 🚀 Getting Started")

        with st.expander("📋 Step-by-Step Guide"):
            st.markdown("""
            1. **Upload Documents**: Go to any feature and upload your PDF, DOCX, or TXT files
            2. **Ask Questions**: Use the Question Answering feature to get instant answers
            3. **Generate Quizzes**: Create practice tests from your materials
            4. **Summarize Content**: Get quick overviews of lengthy documents
            5. **Track Progress**: Monitor your learning journey in the dashboard
            """)

        # Recent activity (demo)
        st.markdown("## 📈 Recent Activity")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>Questions Asked</h4>
                <h2>24</h2>
                <small>+3 today</small>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>Quizzes Taken</h4>
                <h2>8</h2>
                <small>+1 today</small>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>Documents</h4>
                <h2>12</h2>
                <small>+2 this week</small>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div class="metric-card">
                <h4>Study Time</h4>
                <h2>4.5h</h2>
                <small>this week</small>
            </div>
            """, unsafe_allow_html=True)

    def question_answering_interface(self):
        st.markdown("## ❓ Question Answering System")
        st.markdown("Upload your study materials and ask questions to get instant answers.")

        # File upload
        uploaded_file = st.file_uploader(
            "📁 Upload your study material",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )

        if uploaded_file is not None:
            # Display file info
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size} bytes",
                "File type": uploaded_file.type
            }
            st.json(file_details)

            # Simulate document processing
            with st.spinner("🔄 Processing document..."):
                import time
                time.sleep(2)  # Simulate processing time

            st.success("✅ Document processed successfully!")

            # Question input
            st.markdown("### 💭 Ask a Question")
            question = st.text_input(
                "Enter your question:",
                placeholder="What are the main concepts covered in this document?"
            )

            if question:
                with st.spinner("🤔 Finding answer..."):
                    import time
                    time.sleep(1)

                # Demo answer (in real implementation, this would use RAG)
                st.markdown("### 📝 Answer:")
                st.info("""
                Based on your uploaded document, here are the main concepts:

                1. **Key Topic 1**: Explanation of the first main concept
                2. **Key Topic 2**: Description of the second important point  
                3. **Key Topic 3**: Summary of the third major theme

                This answer is generated from the specific sections of your document.
                """)

                st.markdown("### 📚 Sources:")
                st.write("• Page 1, Section 2.1")
                st.write("• Page 3, Section 3.2") 

                # Follow-up questions
                st.markdown("### 🔗 Related Questions:")
                if st.button("Can you elaborate on Key Topic 1?"):
                    st.write("Here's more detail about Key Topic 1...")
        else:
            st.info("👆 Please upload a document to get started with question answering.")

    def quiz_interface(self):
        st.markdown("## 📝 Quiz Generation")
        st.markdown("Generate custom quizzes from your study materials.")

        # File upload for quiz generation
        uploaded_file = st.file_uploader(
            "📁 Upload document for quiz generation",
            type=['pdf', 'docx', 'txt'],
            key="quiz_upload"
        )

        if uploaded_file:
            st.success("✅ Document uploaded for quiz generation!")

            # Quiz configuration
            col1, col2, col3 = st.columns(3)

            with col1:
                num_questions = st.slider("Number of questions:", 5, 20, 10)

            with col2:
                difficulty = st.select_slider(
                    "Difficulty level:",
                    options=["Easy", "Medium", "Hard"],
                    value="Medium"
                )

            with col3:
                question_type = st.selectbox(
                    "Question type:",
                    ["Multiple Choice", "True/False", "Mixed"]
                )

            if st.button("🎯 Generate Quiz", type="primary"):
                with st.spinner("⚡ Generating quiz questions..."):
                    import time
                    time.sleep(3)

                st.markdown("### 📋 Generated Quiz")

                # Demo quiz questions
                quiz_questions = [
                    {
                        "question": "What is the primary purpose of machine learning?",
                        "options": [
                            "A) To replace human intelligence completely",
                            "B) To enable computers to learn and improve from data",
                            "C) To create artificial consciousness",
                            "D) To automate all human tasks"
                        ],
                        "correct": "B",
                        "explanation": "Machine learning focuses on enabling systems to learn and improve from data."
                    },
                    {
                        "question": "Which algorithm is commonly used for classification tasks?",
                        "options": [
                            "A) Linear Regression",
                            "B) K-Means Clustering", 
                            "C) Random Forest",
                            "D) Principal Component Analysis"
                        ],
                        "correct": "C",
                        "explanation": "Random Forest is a popular ensemble method for classification."
                    }
                ]

                for i, q in enumerate(quiz_questions, 1):
                    st.markdown(f"**Question {i}:** {q['question']}")

                    # Create radio buttons for answers
                    user_answer = st.radio(
                        "Select your answer:",
                        q["options"],
                        key=f"q{i}",
                        label_visibility="collapsed"
                    )

                    if st.button(f"Check Answer {i}", key=f"check{i}"):
                        correct_option = next(opt for opt in q["options"] if opt.startswith(q["correct"]))
                        if user_answer == correct_option:
                            st.success(f"✅ Correct! {q['explanation']}")
                        else:
                            st.error(f"❌ Incorrect. The correct answer is {q['correct']}. {q['explanation']}")

                    st.markdown("---")
        else:
            st.info("👆 Please upload a document to generate quiz questions.")

    def summarization_interface(self):
        st.markdown("## 📄 Text Summarization")
        st.markdown("Generate concise summaries of your study materials.")

        # Input method selection
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
                st.success("✅ File uploaded successfully!")
                text_content = "Sample document content would be extracted here..."

        else:
            text_content = st.text_area(
                "📝 Paste your text here:",
                height=200,
                placeholder="Enter the text you want to summarize..."
            )

        if text_content:
            # Summarization options
            col1, col2, col3 = st.columns(3)

            with col1:
                summary_length = st.select_slider(
                    "Summary length:",
                    options=["Short", "Medium", "Long"],
                    value="Medium"
                )

            with col2:
                summary_type = st.selectbox(
                    "Summary type:",
                    ["Extractive", "Abstractive"]
                )

            with col3:
                include_keywords = st.checkbox("Include key points", value=True)

            if st.button("📄 Generate Summary", type="primary"):
                with st.spinner("⚡ Generating summary..."):
                    import time
                    time.sleep(2)

                # Demo summary
                st.markdown("### 📋 Generated Summary")
                st.info("""
                **Summary:**
                This document covers the fundamental concepts of artificial intelligence and machine learning. 
                Key topics include supervised learning algorithms, neural networks, and practical applications 
                in various industries. The content emphasizes the importance of data quality and ethical 
                considerations in AI development.
                """)

                if include_keywords:
                    st.markdown("### 🔑 Key Points")
                    st.write("• Artificial Intelligence fundamentals")
                    st.write("• Machine Learning algorithms") 
                    st.write("• Neural Networks architecture")
                    st.write("• Data quality importance")
                    st.write("• Ethical AI considerations")

                # Summary statistics
                st.markdown("### 📊 Summary Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Original Length", "1,500 words")
                with col2:
                    st.metric("Summary Length", "75 words")  
                with col3:
                    st.metric("Compression Ratio", "95%")

        else:
            st.info("👆 Please provide text content to generate a summary.")

    def progress_dashboard(self):
        st.markdown("## 📊 Progress Dashboard")
        st.markdown("Track your learning journey and performance.")

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📚 Total Questions",
                "127",
                delta="12",
                delta_color="normal"
            )

        with col2:
            st.metric(
                "🎯 Accuracy Rate",
                "84%",
                delta="3%",
                delta_color="normal"
            )

        with col3:
            st.metric(
                "⏱️ Study Time",
                "15.5h",
                delta="2.5h",
                delta_color="normal"
            )

        with col4:
            st.metric(
                "📈 Streak",
                "7 days",
                delta="1 day",
                delta_color="normal"
            )

        st.markdown("---")

        # Progress charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📈 Weekly Progress")
            # Sample data for demo
            import pandas as pd
            import random

            dates = pd.date_range("2024-01-01", periods=7)
            progress_data = pd.DataFrame({
                "Date": dates,
                "Questions": [random.randint(5, 15) for _ in range(7)],
                "Accuracy": [random.uniform(0.7, 0.95) for _ in range(7)]
            })

            st.line_chart(progress_data.set_index("Date"))

        with col2:
            st.markdown("### 🎯 Subject Performance")
            subject_data = pd.DataFrame({
                "Subject": ["Mathematics", "Physics", "Chemistry", "Biology"],
                "Score": [85, 92, 78, 88]
            })
            st.bar_chart(subject_data.set_index("Subject"))

        # Recent achievements
        st.markdown("### 🏆 Recent Achievements")

        achievements = [
            {"icon": "🎯", "title": "Quiz Master", "desc": "Completed 10 quizzes with >80% accuracy"},
            {"icon": "📚", "title": "Knowledge Seeker", "desc": "Asked 50 questions this month"},
            {"icon": "⚡", "title": "Speed Reader", "desc": "Summarized 5 documents in one day"},
            {"icon": "🔥", "title": "Study Streak", "desc": "7 days of consistent studying"}
        ]

        for achievement in achievements:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"## {achievement['icon']}")
            with col2:
                st.markdown(f"**{achievement['title']}**")
                st.markdown(achievement['desc'])
            st.markdown("---")

if __name__ == "__main__":
    app = StudyAssistantApp()
    app.main()
