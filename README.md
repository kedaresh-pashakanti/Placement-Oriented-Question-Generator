# Placement-Oriented Question Generator

### Problem Statement
The placement preparation process for engineering and IT graduates faces several challenges:

- Limited access to **company-specific practice questions**  
- Difficulty in getting **realistic interview Q&A**  
- Lack of **personalized question difficulty adjustment**  
- Time-consuming process of **creating and evaluating practice tests**  
- Need for **comprehensive coverage** across Aptitude, Technical, and Interview rounds  

This project addresses these challenges by providing an **AI-powered quiz generation system** that creates **customized practice questions for placement preparation** across top IT companies.

---

### Industry Applications

1. **Education & Training**
   - Placement training institutes  
   - Online learning platforms  
   - Self-study programs for students  

2. **Corporate Hiring Preparation**
   - Campus recruitment training  
   - Company-specific interview practice  
   - Mock interview simulations  

3. **Assessment Tools**
   - HR training platforms  
   - Skill evaluation systems  
   - Candidate screening platforms  

---

## Tools & Technologies Used

### Core Technologies
- **Python 3.10+**  
- **Streamlit** (for web interface)  
- **Groq LLM API** (for question generation)  
- **Pandas** (for data handling)  

### Libraries & Frameworks
- **langchain-groq**  
- **pydantic**  
- **python-dotenv**  
- **streamlit**  
- **pandas**  

### Development Tools
- VSCode / PyCharm (recommended IDE)  
- Git (version control)  
- Virtual Environment (venv / conda)  

---

## Project Setup

1. **Clone the Repository**
```bash
git clone <repository-url>
cd placement-quiz-generator
```

2. **Create Virtual Environment**
```bash
conda create -p env python=3.10 -y
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**  
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the Application**
```bash
streamlit run app.py
```

---

### Project Structure
```bash
├── app.py                # Main Streamlit application
├── utils.py              # Question generator utilities (MCQs + Interview Q&A)
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables
├── results/              # Generated quiz results
└── README.md             # Project documentation
```

---

### Features

1. **Company-Specific Question Generation**
   - Supports **Accenture, Wipro, TCS, Infosys, Amazon, Deloitte, IBM, Tech Mahindra, Capgemini, Cognizant, Hexaware, Saint Gobain, CTS**
   - Auto-generates placement-oriented questions  

2. **Question Rounds**
   - **Aptitude MCQs** (Quantitative, DI, Reasoning, Verbal, Non-Verbal)  
   - **Technical MCQs** (Python, Java, C/C++, SQL, DSA, DBMS, OS, CN, React, Angular)  
   - **Interview Questions (HR-style)** with **best suitable answers**  

3. **Difficulty Control**
   - Easy / Medium / Hard (for MCQs)  

4. **Quiz Management**
   - Interactive quiz interface  
   - Auto evaluation of MCQs  
   - HR Interview answers shown for guidance  

5. **Result Analysis**
   - Score calculation & performance metrics  
   - Save quiz results to CSV  
   - Download results  

---

### Future Enhancements

1. **Technical Improvements**
   - Question caching for faster generation  
   - Support for multiple LLM providers  
   - Enhanced de-duplication & variety in Q&A  

2. **Feature Additions**
   - More question types (True/False, Coding Challenges, Group Discussion prompts)  
   - Auto adaptive difficulty adjustment  
   - Topic-wise performance analytics  

3. **User Experience**
   - Dark mode support  
   - Mobile-friendly UI  
   - User login & profiles  

4. **Content & Integration**
   - Pre-built company question banks  
   - Integration with mock test platforms  
   - Peer-to-peer quiz sharing  

---

👉 This project aims to **revolutionize placement preparation** by combining **AI-powered question generation** with **company-specific focus** for Aptitude, Technical, and HR Interview rounds. 🚀  
