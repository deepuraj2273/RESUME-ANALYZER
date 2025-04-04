import streamlit as st
import os
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
import docx2txt
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import time

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Set Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Initialize the Hugging Face client
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token="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"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background: linear-gradient(45deg, #1a73e8, #4285f4);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.2);
    }
    .stFileUploader>div>div>div>div {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 2px dashed #e0e0e0;
    }
    .stMarkdown h1 {
        color: #1a73e8;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .stMarkdown h2 {
        color: #1a73e8;
        margin-top: 2rem;
        font-weight: 600;
    }
    .stMarkdown h3 {
        color: #1a73e8;
        font-weight: 600;
    }
    .stMarkdown p {
        color: #333333;
    }
    .success-box {
        background: linear-gradient(45deg, #34a853, #4caf50);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(52, 168, 83, 0.2);
    }
    .info-box {
        background: linear-gradient(45deg, #1a73e8, #4285f4);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(26, 115, 232, 0.2);
    }
    .analysis-box {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin: 1rem 0;
        border-left: 4px solid #1a73e8;
        color: #333333;
    }
    .section-title {
        color: #1a73e8;
        font-weight: 700;
        margin-top: 1.5rem;
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #1a73e8;
    }
    .ats-tips {
        background: linear-gradient(45deg, #fbbc05, #f9ab00);
        color: #333333;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(251, 188, 5, 0.2);
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.3s ease;
        color: #333333;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }
    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin: 2rem 0;
        color: #333333;
    }
    .header-section {
        background: linear-gradient(45deg, #1a73e8, #4285f4);
        padding: 3rem 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(26, 115, 232, 0.2);
    }
    .analysis-text {
        color: #333333;
        line-height: 1.6;
    }
    .feature-text {
        color: #333333;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_file(file):
    """Extract text from different file formats"""
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension == '.pdf':
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    elif file_extension == '.docx':
        return docx2txt.process(file)
    
    elif file_extension == '.txt':
        return file.read().decode('utf-8')
    
    else:
        raise ValueError("Unsupported file format")

def analyze_resume(resume_text):
    """Analyze the resume using the LLM"""
    prompt = f"""<s>[INST] You are a professional resume analyzer and ATS optimization expert. Analyze the following resume and provide a detailed professional assessment with specific focus on ATS optimization.

Resume Content:
{resume_text}

Please provide a comprehensive analysis with the following sections:

1. Key Skills and Technical Expertise:
- List the main technical skills
- Highlight domain expertise
- Note any certifications
- ATS Optimization: Check if skills match job descriptions

2. Professional Experience:
- Summarize years of experience
- Key roles and responsibilities
- Industry exposure
- ATS Optimization: Check for action verbs and quantifiable achievements

3. Education and Qualifications:
- Academic background
- Professional certifications
- Additional training
- ATS Optimization: Verify proper formatting and relevance

4. Notable Achievements:
- Key accomplishments
- Projects and their impact
- Recognition and awards
- ATS Optimization: Check for quantifiable results

5. ATS Optimization Score and Tips:
- Current ATS compatibility score (1-10)
- Specific ATS optimization recommendations
- Keyword optimization suggestions
- Formatting improvements
- Common ATS pitfalls to avoid

6. Areas for Improvement:
- Skills gaps
- Missing certifications
- Presentation suggestions
- ATS-specific improvements

7. Career Recommendations:
- Suitable job roles
- Industry fit
- Growth opportunities
- ATS-friendly job titles

8. Actionable ATS Optimization Steps:
- Immediate improvements needed
- Long-term optimization strategy
- Keyword suggestions for target roles
- Formatting best practices

Provide the analysis in a clear, structured format with specific focus on ATS optimization and improvement suggestions. [/INST]"""

    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=1024,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
            repetition_penalty=1.1
        )
        return response
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        return None

def main():
    # Header with gradient background
    st.markdown("""
    <div class='header-section'>
        <h1 style='color: white; text-align: center; margin: 0; font-size: 2.5rem;'>📄 Professional Resume Analyzer</h1>
        <p style='color: white; text-align: center; margin: 1rem 0 0 0; font-size: 1.2rem;'>AI-Powered Resume Analysis & ATS Optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction section
    st.markdown("""
    <div class='info-box'>
        <h2 style='color: white; margin-top: 0;'>Welcome to Your Career Success Partner!</h2>
        <p style='color: white; font-size: 1.1rem;'>Get instant, professional feedback on your resume and discover new career opportunities with our AI-powered analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>✨</div>
            <h3>Smart Analysis</h3>
            <p class='feature-text'>AI-powered insights into your resume</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🎯</div>
            <h3>ATS Optimization</h3>
            <p class='feature-text'>Improve your resume's ATS score</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <h3>Detailed Feedback</h3>
            <p class='feature-text'>Comprehensive improvement suggestions</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🚀</div>
            <h3>Career Guidance</h3>
            <p class='feature-text'>Personalized career recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # File upload section
    st.markdown("""
    <div class='upload-section'>
        <h2 style='color: #1a73e8; margin-top: 0;'>Upload Your Resume</h2>
        <p style='color: #333333;'>Supported formats: PDF, DOCX, TXT</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose your resume file", type=['pdf', 'docx', 'txt'], label_visibility="visible")
    
    if uploaded_file is not None:
        try:
            with st.spinner("📄 Processing your resume..."):
                resume_text = extract_text_from_file(uploaded_file)
                
                if st.button("🔍 Analyze Resume", key="analyze_button"):
                    with st.spinner("🤖 AI is analyzing your resume... This may take a few moments."):
                        analysis = analyze_resume(resume_text)
                        
                        if analysis:
                            st.markdown("""
                            <div class='success-box'>
                                <h2 style='color: white; margin: 0;'>✅ Analysis Complete!</h2>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display analysis results
                            st.markdown("### 📊 Analysis Results")
                            st.markdown("---")
                            
                            # Display the analysis in a more readable format
                            sections = analysis.split('\n\n')
                            for section in sections:
                                if section.strip():
                                    if "ATS Optimization Score" in section:
                                        st.markdown(f"""
                                        <div class='ats-tips'>
                                            <div class='analysis-text'>{section.strip()}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"""
                                        <div class='analysis-box'>
                                            <div class='analysis-text'>{section.strip()}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            
                            # Download button with modern styling
                            st.download_button(
                                label="📥 Download Analysis Report",
                                data=analysis,
                                file_name="resume_analysis_report.txt",
                                mime="text/plain",
                                key="download_button"
                            )
                        
        except Exception as e:
            st.error(f"❌ Error processing the file: {str(e)}")
            st.markdown("""
            <div class='info-box'>
                <h3 style='color: white; margin-top: 0;'>Common Solutions:</h3>
                <ol style='color: white;'>
                    <li>Make sure the file is not corrupted</li>
                    <li>Try converting to a different format (PDF, DOCX, or TXT)</li>
                    <li>Ensure the file is properly formatted</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
