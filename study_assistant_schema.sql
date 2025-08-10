
-- Users table to store student information
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    study_streak INTEGER DEFAULT 0,
    total_study_time INTEGER DEFAULT 0
);

-- Documents table to store uploaded study materials
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    content_preview TEXT,
    word_count INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Study sessions table to track user activity
CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    duration_minutes INTEGER,
    activities_count INTEGER DEFAULT 0,
    documents_accessed TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Questions table to store generated questions
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL, -- 'mcq', 'true_false', 'short_answer'
    difficulty_level TEXT DEFAULT 'medium', -- 'easy', 'medium', 'hard'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_chunk TEXT,
    FOREIGN KEY (document_id) REFERENCES documents (id)
);

-- Quiz responses table to track user answers
CREATE TABLE quiz_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    user_answer TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    response_time_seconds INTEGER,
    session_id INTEGER,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (question_id) REFERENCES questions (id),
    FOREIGN KEY (session_id) REFERENCES study_sessions (id)
);

-- Summaries table to store generated summaries
CREATE TABLE summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    summary_text TEXT NOT NULL,
    summary_type TEXT DEFAULT 'auto', -- 'auto', 'custom'
    length_setting TEXT DEFAULT 'medium', -- 'short', 'medium', 'long'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    key_points TEXT,
    FOREIGN KEY (document_id) REFERENCES documents (id)
);

-- Progress tracking table for detailed analytics
CREATE TABLE progress_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    questions_answered INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    study_time_minutes INTEGER DEFAULT 0,
    documents_read INTEGER DEFAULT 0,
    summaries_generated INTEGER DEFAULT 0,
    average_response_time REAL,
    topics_covered TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- User preferences and settings
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    quiz_difficulty TEXT DEFAULT 'medium',
    summary_length TEXT DEFAULT 'medium',
    daily_study_goal INTEGER DEFAULT 30,
    reminder_enabled BOOLEAN DEFAULT 1,
    theme_preference TEXT DEFAULT 'light',
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_study_sessions_user_id ON study_sessions(user_id);
CREATE INDEX idx_questions_document_id ON questions(document_id);
CREATE INDEX idx_quiz_responses_user_id ON quiz_responses(user_id);
CREATE INDEX idx_progress_tracking_user_date ON progress_tracking(user_id, date);
