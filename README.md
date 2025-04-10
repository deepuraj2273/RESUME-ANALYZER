# Resume Analyzer

![Resume Analyzer](https://img.shields.io/badge/Status-Active-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

A modern, AI-powered resume analysis tool that helps optimize resumes for Applicant Tracking Systems (ATS) and provides comprehensive feedback for job seekers.

## 🌟 Features

- **Smart Resume Analysis**: Leverages Mistral-7B AI model for in-depth resume evaluation
- **Multi-Format Support**: Handles PDF, DOCX, and TXT file formats
- **ATS Optimization**: Provides detailed ATS compatibility scoring and improvement suggestions
- **Comprehensive Analysis**: Evaluates skills, experience, education, and achievements
- **Modern UI**: Clean, responsive interface built with Streamlit
- **Actionable Insights**: Delivers specific recommendations for resume improvement

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd resume-analyzer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root and add your Hugging Face API token:
```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

4. Run the application:
```bash
streamlit run resumeanalyzer.py
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: 
  - Hugging Face's Mistral-7B model
  - LangChain framework
- **File Processing**: 
  - PyPDF2 for PDF files
  - docx2txt for DOCX files
- **Styling**: Custom CSS with modern UI elements

## 📋 Features in Detail

1. **Resume Analysis**
   - Skills and technical expertise evaluation
   - Professional experience assessment
   - Education and qualifications review
   - Achievement analysis

2. **ATS Optimization**
   - ATS compatibility scoring
   - Keyword optimization suggestions
   - Formatting recommendations
   - Common pitfall identification

3. **Career Guidance**
   - Suitable job role recommendations
   - Industry fit analysis
   - Growth opportunity identification
   - Career path suggestions

## 🔧 Configuration

The application uses the following key configurations:

- Streamlit page configuration with wide layout
- Custom CSS styling for modern UI
- Hugging Face API integration
- File upload size limits and supported formats

## 📝 Usage

1. Launch the application
2. Upload your resume (PDF, DOCX, or TXT format)
3. Wait for the AI analysis to complete
4. Review the comprehensive analysis including:
   - ATS optimization score
   - Key skills assessment
   - Professional experience evaluation
   - Improvement recommendations
   - Career guidance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Mistral AI for the language model
- Streamlit for the web framework
- Hugging Face for model hosting
- LangChain for the AI framework
