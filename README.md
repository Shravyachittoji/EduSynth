# 🎓 EduSynth - Adaptive AI Learning System

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**EduSynth** is an intelligent, personalized learning platform powered by AI that dynamically generates educational content tailored to each student's learning level and pace. It combines generative AI, machine learning, and interactive learning features to create an adaptive educational experience.

---

## 🌟 Key Features

### 📚 **Adaptive Learning Path**
- AI-powered content generation using Google Gemini 2.5 Flash
- Personalized learning experiences for Beginner, Intermediate, and Advanced levels
- Dynamic topic progression with structured curriculum
- Real-time explanations with real-world examples

### 📝 **Interactive Quiz Engine**
- Automatically generated quizzes based on subjects and difficulty levels
- Real-time performance tracking
- Instant feedback and score analytics

### 💻 **Coding Practice Module**
- AI-generated coding challenges across multiple subjects
- Integrated code execution environment with sandbox testing
- Automated evaluation with test case validation
- Multi-level difficulty progression (Beginner, Intermediate, Advanced)

### 💬 **Doubt Resolution System**
- Ask subject-specific questions in real-time
- AI-powered instant responses using Gemini API
- Question history and retrieval system
- Subject-wise doubt tracking

### 📊 **Performance Analytics**
- Comprehensive progress tracking and visualization
- Subject comparison charts
- PDF performance report generation
- Historical performance data with detailed metrics
- Research-backed model analytics dashboard

### 🔐 **User Authentication**
- Secure registration and login system
- Password encryption with bcrypt
- SQLite-based user database
- Session management

### 📈 **Knowledge Level Prediction**
- Machine Learning model (Random Forest Classifier)
- Predicts student knowledge levels based on:
  - Quiz performance
  - Time spent on topics
  - Number of attempts
  - Historical accuracy
- **Model Accuracy**: 94.6% (trained on 1,200+ students dataset)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Backend** | Python |
| **AI/LLM** | Google Gemini 2.5 Flash API |
| **Database** | SQLite3 |
| **ML Models** | Scikit-learn (Random Forest, Decision Trees, SVM) |
| **Code Execution** | Python subprocess sandbox |
| **Report Generation** | ReportLab |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Streamlit Charts |
| **Security** | bcrypt |

---

## 📋 Subjects & Topics Covered

- **Python Programming**: 
  - Introduction to Python
  - Variables and Data Types
  - Control Structures
  - Functions
  - Object-Oriented Programming

- **Data Structures**: 
  - Introduction to Data Structures
  - Arrays
  - Linked Lists
  - Stacks
  - Queues

- **Machine Learning**: 
  - What is Machine Learning?
  - Supervised Learning
  - Unsupervised Learning
  - Model Training
  - Evaluation Metrics

- **Artificial Intelligence**: 
  - Introduction to AI
  - Search Algorithms
  - Knowledge Representation
  - Neural Networks
  - Ethics in AI

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shravyachittoji/EduSynth.git
   cd EduSynth
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   - Get your Google Gemini API key from [Google AI Studio](https://ai.google.dev/)
   - Update the `main.py` file with your API key:
     ```python
     genai.configure(api_key="YOUR_API_KEY_HERE")
     ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

6. **Access the app**
   - Open your browser and navigate to `http://localhost:8501`

---

## 📁 Project Structure

```
EduSynth/
├── main.py                    # Main Streamlit application & routing
├── auth.py                    # User authentication (login/register)
├── learning_flow.py           # AI-powered learning content generation
├── quiz_engine.py             # Quiz generation & evaluation
├── coding_practice.py         # Coding challenges & execution
├── doubts.py                  # Doubt resolution system
├── progress.py                # Performance tracking & PDF reports
├── subject_comparison.py       # Subject-wise analytics
├── analytics.py               # Research analytics & model benchmarks
├── database.py                # SQLite database operations
├── train_model.py             # ML model training script
├── backend/
│   └── predict.py             # Knowledge level prediction engine
├── models/                    # Trained ML models
│   ├── knowledge_model.pkl
│   └── label_encoder.pkl
├── data/
│   └── student_data.csv       # Training dataset
├── students.db                # SQLite database
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🎯 Usage Guide

### 1. **Registration & Login**
   - Create a new account with name, email, and password
   - Secure password hashing using bcrypt
   - Login with credentials

### 2. **Select Subject & Level**
   - Choose from 4 subjects (Python, Data Structures, Machine Learning, Artificial Intelligence)
   - Select difficulty level (Beginner, Intermediate, Advanced)

### 3. **Learn**
   - Engage with AI-generated explanations for each topic
   - Real-world examples for context and practical understanding
   - Progressive topic navigation (Previous/Next buttons)
   - Structured learning flow with clear progression

### 4. **Practice**
   - **Quizzes**: Auto-generated questions with instant feedback
   - **Coding**: Write and execute code in a sandboxed environment
   - **Doubts**: Ask questions and get instant AI-powered responses

### 5. **Track Progress**
   - View detailed performance analytics
   - Compare performance across subjects
   - Download PDF performance reports
   - Monitor knowledge level predictions

---

## 📊 Model Performance

The EduSynth knowledge prediction model demonstrates strong performance:

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| **EduSynth (Random Forest)** | **94.6%** | **93%** | **92%** | **93%** |
| Logistic Regression | 85.2% | 84% | 83% | 83.5% |
| Decision Tree | 89.1% | 88% | 87% | 87.5% |
| SVM | 90.8% | 90% | 89% | 89.5% |

### Feature Importance
- Attendance %: 28%
- Assignment Completion: 24%
- Quiz Performance: 21%
- Participation Metrics: 17%
- Historical GPA: 10%

---

## 📦 Dependencies

```
streamlit          # Web UI framework
google-generativeai # Google Gemini API integration
bcrypt            # Password hashing
reportlab         # PDF report generation
plotly            # Advanced data visualization
pandas            # Data manipulation
numpy             # Numerical computing
scikit-learn      # Machine learning models
```

See `requirements.txt` for detailed versions.

---

## 🔧 Configuration

### Modifying Subjects & Topics
Edit the `topic_map` dictionary in `learning_flow.py`:
```python
topic_map = {
    "Python": ["Introduction to Python", "Variables and Functions", ...],
    "Data Structures": ["Introduction to Data Structures", "Arrays", ...],
    # Modify or add more subjects and topics
}
```

### Adjusting Quiz Difficulty
Modify prompt parameters in `quiz_engine.py` to control question complexity and style

### Training Custom ML Models
Run the training script:
```bash
python train_model.py
```

---

## 🔐 Security Features

- ✅ Bcrypt password hashing (secure password storage)
- ✅ SQLite database with user isolation
- ✅ Session-based authentication
- ✅ Secure API key management
- ✅ Sandboxed code execution (prevents arbitrary system access)
- ✅ Input validation

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋 Support & Contact

- **GitHub**: [@Shravyachittoji](https://github.com/Shravyachittoji)
- **Repository**: [EduSynth](https://github.com/Shravyachittoji/EduSynth)
- **Issues**: [Report bugs or request features](https://github.com/Shravyachittoji/EduSynth/issues)

---

## 🎓 Research Paper

EduSynth is based on research in personalized learning and generative AI for education:
- **Focus**: Generative content creation for personalized learning
- **Dataset**: 1,200+ students
- **Methodology**: Machine Learning with feature importance analysis

---

## 🚧 Roadmap

- [ ] Mobile application
- [ ] Real-time collaboration features
- [ ] Advanced plagiarism detection for coding
- [ ] Integration with popular LMS platforms
- [ ] Multi-language support
- [ ] Gamification features
- [ ] Parent/teacher dashboard
- [ ] Certificate generation
- [ ] Video content generation

---

## 💡 Key Highlights

🎯 **Personalized Learning**: Every student gets a unique learning path  
⚡ **AI-Powered**: Powered by Google Gemini for intelligent content generation  
📊 **Data-Driven**: ML models predict student knowledge levels with 94.6% accuracy  
🔄 **Adaptive**: Content difficulty adjusts based on student performance  
🛡️ **Secure**: Enterprise-grade authentication and data security  
📱 **User-Friendly**: Intuitive interface with modern UI/UX built with Streamlit  
💻 **Hands-On**: Integrated coding practice with live code execution  

---

## 📞 Feedback

We'd love to hear from you! Please share your feedback and suggestions by opening an issue on GitHub.

---

<div align="center">

**Made with ❤️ for better education**

⭐ If you find this project helpful, please consider giving it a star!

</div>
